# -*- coding: utf-8 -*-
"""
Lớp gọi API của các nhà cung cấp AI.

Đây là chỗ duy nhất trong dự án biết cách nói chuyện với Gemini và Claude.
Phần còn lại của công cụ chỉ gọi `viet_bai()` và nhận về KetQua — nên sau này
thêm nhà cung cấp thứ ba chỉ cần thêm một lớp ở file này.
"""

import json
import re
import time
from dataclasses import dataclass
from typing import List, Optional

import requests

from . import config
from .logger import lay_log
from .settings import Settings

log = lay_log()

URL_GEMINI = "https://generativelanguage.googleapis.com/v1beta"

# Gói miễn phí hay bị quá tải tạm thời -> tự thử lại vài lần trước khi báo lỗi.
SO_LAN_THU_LAI = 3
GIAY_CHO_GIUA_CAC_LAN = 8


class LoiGoiAI(Exception):
    """Lỗi khi gọi API. Thông điệp đã được viết lại cho người không rành kỹ thuật."""


@dataclass
class KetQua:
    """Kết quả một lần gọi AI."""

    noi_dung: str
    model: str
    token_vao: int = 0
    token_ra: int = 0

    def chi_phi_usd(self, st: Settings) -> Optional[float]:
        """Ước tính chi phí. None nếu không biết đơn giá."""
        gia = st.bang_gia()
        if gia is None:
            return None
        return (self.token_vao * gia["vao"] + self.token_ra * gia["ra"]) / 1_000_000

    def mo_ta_chi_phi(self, st: Settings) -> str:
        """Chuỗi hiển thị chi phí trên giao diện."""
        usd = self.chi_phi_usd(st)
        if usd is None:
            return f"{self.token_ra:,} token"
        if usd == 0:
            return f"{self.token_ra:,} token · miễn phí"
        vnd = usd * config.TY_GIA_VND
        return f"{self.token_ra:,} token · ~{vnd:,.0f}đ"


# =============================================================================
# GOOGLE GEMINI
# =============================================================================

class NhaCungCapGemini:
    """Gọi Google Gemini qua REST. Không cần cài thêm thư viện nào."""

    def __init__(self, st: Settings):
        self.st = st

    def viet_bai(self, prompt: str, nen_dung=None) -> KetQua:
        """
        Gọi Gemini, tự thử lại khi model quá tải.

        Gói miễn phí dùng chung tài nguyên với rất nhiều người nên hay gặp
        503 "high demand" — lỗi tạm thời, chờ vài giây là qua. Đã gặp thật
        khi test, nên tự thử lại thay vì bắt người dùng bấm đi bấm lại.
        """
        url = f"{URL_GEMINI}/models/{self.st.model}:generateContent"
        than_yeu_cau = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"maxOutputTokens": self.st.max_tokens},
        }

        for lan_thu in range(1, SO_LAN_THU_LAI + 1):
            if nen_dung is not None and nen_dung():
                raise LoiGoiAI("Đã dừng theo yêu cầu.")

            try:
                phan_hoi = requests.post(
                    url,
                    headers={
                        "x-goog-api-key": self.st.api_key,
                        "Content-Type": "application/json",
                    },
                    json=than_yeu_cau,
                    timeout=self.st.timeout,
                )
            except requests.Timeout:
                raise LoiGoiAI(
                    f"Quá {self.st.timeout} giây chưa thấy hồi âm.\n"
                    f"Thử tăng TIMEOUT trong file .env, hoặc kiểm tra mạng."
                ) from None
            except requests.RequestException as loi:
                raise LoiGoiAI(f"Không kết nối được tới Google: {loi}") from None

            if phan_hoi.status_code == 200:
                return self._doc_ket_qua(phan_hoi.json())

            # Chỉ thử lại với lỗi TẠM THỜI. Sai key hay sai tên model thì có
            # thử bao nhiêu lần cũng vậy, báo ngay cho người dùng biết.
            la_tam_thoi = phan_hoi.status_code in (429, 500, 503)

            # Hết hạn mức NGÀY thì thử lại chỉ tốn thêm lượt của model khác và
            # kéo dài thời gian chờ vô ích — dừng ngay để báo cách gỡ.
            if phan_hoi.status_code == 429:
                chi_tiet = self._boc_chi_tiet_han_muc(phan_hoi)
                if "PerDay" in chi_tiet.get("quota_id", ""):
                    raise LoiGoiAI(self._giai_thich_loi(phan_hoi))

            if not la_tam_thoi or lan_thu == SO_LAN_THU_LAI:
                raise LoiGoiAI(self._giai_thich_loi(phan_hoi))

            if phan_hoi.status_code == 429:
                # Hạn mức theo phút: nghe theo con số Google đưa, cộng 2 giây đệm.
                cho = (self._boc_chi_tiet_han_muc(phan_hoi).get("cho_giay") or 30) + 2
            else:
                cho = GIAY_CHO_GIUA_CAC_LAN * lan_thu     # 8s -> 16s -> 24s

            log.warning("Model đang bận (lỗi %d). Tự thử lại lần %d/%d sau %d giây...",
                        phan_hoi.status_code, lan_thu + 1, SO_LAN_THU_LAI, cho)
            time.sleep(cho)

        raise LoiGoiAI("Không gọi được Gemini sau nhiều lần thử.")

    # ------------------------------------------------------------------

    def _doc_ket_qua(self, du_lieu: dict) -> KetQua:
        """Bóc nội dung bài viết ra khỏi JSON Gemini trả về."""
        cac_ung_vien = du_lieu.get("candidates") or []
        if not cac_ung_vien:
            raise LoiGoiAI(
                "Gemini không trả về nội dung nào.\n"
                "Thường do bộ lọc an toàn chặn. Thử sửa lại prompt cho trung tính hơn."
            )

        ung_vien = cac_ung_vien[0]
        cac_phan = (ung_vien.get("content") or {}).get("parts") or []
        noi_dung = "".join(p.get("text", "") for p in cac_phan).strip()

        if not noi_dung:
            ly_do = ung_vien.get("finishReason", "không rõ")
            if ly_do == "MAX_TOKENS":
                raise LoiGoiAI(
                    "Bài viết bị cắt ngay từ đầu vì chạm giới hạn độ dài.\n"
                    "Tăng MAX_TOKENS trong file .env."
                )
            raise LoiGoiAI(f"Gemini trả về rỗng (lý do: {ly_do}).")

        thong_ke = du_lieu.get("usageMetadata") or {}
        return KetQua(
            noi_dung=noi_dung,
            model=self.st.model,
            token_vao=thong_ke.get("promptTokenCount", 0),
            token_ra=thong_ke.get("candidatesTokenCount", 0),
        )

    def _giai_thich_loi(self, phan_hoi) -> str:
        """Đổi mã lỗi HTTP thành câu tiếng Việt kèm cách xử lý."""
        ma = phan_hoi.status_code
        try:
            chi_tiet = phan_hoi.json().get("error", {}).get("message", "")
        except (ValueError, json.JSONDecodeError):
            chi_tiet = phan_hoi.text[:200]

        if ma in (400, 403) and "API key" in chi_tiet:
            return ("API key không hợp lệ.\n"
                    "Kiểm tra lại GEMINI_API_KEY trong file .env.\n"
                    "Lấy key mới tại https://aistudio.google.com")

        if ma == 404:
            # Google thường nói thẳng tên model thay thế ngay trong thông điệp,
            # ví dụ: "gemini-2.5-flash is no longer available to new users.
            #         Please update your code to use models/gemini-3.6-flash".
            # Nên ƯU TIÊN đưa nguyên văn câu đó cho người dùng — nó chính xác
            # hơn danh sách tự liệt kê, vì ListModels vẫn trả về cả những model
            # đã ngừng mở cho người dùng mới.
            ten_thay_the = self._tim_model_thay_the(chi_tiet)
            if ten_thay_the:
                return (f"Model '{self.st.model}' không dùng được nữa.\n\n"
                        f"Google đề xuất thay bằng:  {ten_thay_the}\n\n"
                        f"Mở file .env, sửa dòng GEMINI_MODEL thành:\n"
                        f"GEMINI_MODEL={ten_thay_the}")

            ds = self.liet_ke_model()
            goi_y = "\n".join(f"  {m}" for m in ds[:15]) if ds else "  (không lấy được danh sách)"
            return (f"Không tìm thấy model '{self.st.model}'.\n\n"
                    f"Google báo: {chi_tiet}\n\n"
                    f"Các model tài khoản bạn đang dùng được:\n{goi_y}\n\n"
                    f"Chọn một cái, sửa dòng GEMINI_MODEL trong file .env.")

        if ma == 429:
            return self._giai_thich_het_han_muc(phan_hoi)

        if ma in (500, 503):
            return (f"Model '{self.st.model}' đang quá tải.\n\n"
                    f"Đây là lỗi phía Google, không phải lỗi của bạn.\n"
                    f"Chờ vài phút rồi bấm Viết lại, hoặc đổi tạm sang model khác "
                    f"trong file .env.")

        return f"Google báo lỗi {ma}: {chi_tiet}"

    def _giai_thich_het_han_muc(self, phan_hoi) -> str:
        """
        Giải thích lỗi 429 cho đúng bản chất.

        Google phân biệt hai loại hạn mức, xử lý khác hẳn nhau:
          - Theo PHÚT: chờ vài chục giây là dùng tiếp được.
          - Theo NGÀY : chờ bao lâu trong hôm nay cũng vô ích.

        Bản đầu gộp chung, khuyên "chờ ít phút rồi thử lại" cho cả hai — sai
        hoàn toàn với hạn mức ngày. Đã gặp thật: gemini-3.6-flash giới hạn
        20 lượt/ngày, retry 8s rồi 16s chỉ tốn thêm 2 lượt vô ích.

        Điểm mấu chốt: hạn mức tính RIÊNG cho từng model. Hết model này vẫn
        còn model khác, nên gợi ý đổi model là cách gỡ nhanh nhất.
        """
        chi_tiet = self._boc_chi_tiet_han_muc(phan_hoi)
        theo_ngay = "PerDay" in chi_tiet.get("quota_id", "")
        gioi_han = chi_tiet.get("gioi_han")
        mo_ta_gioi_han = f" ({gioi_han} lượt/ngày)" if gioi_han and theo_ngay else ""

        if not theo_ngay:
            cho = chi_tiet.get("cho_giay") or 60
            return (f"Chạm giới hạn theo phút của gói miễn phí.\n"
                    f"Chờ khoảng {cho} giây rồi bấm Viết lại.")

        con_dung = self.tim_model_con_han_muc()
        if con_dung:
            ds = "\n".join(f"    GEMINI_MODEL={m}" for m in con_dung[:4])
            goi_y = (f"Hạn mức tính RIÊNG cho từng model, nên đổi model là dùng tiếp được ngay.\n"
                     f"Mở file .env, sửa dòng GEMINI_MODEL thành một trong các model còn hạn mức:\n\n"
                     f"{ds}")
        else:
            goi_y = ("Các model đã thử đều hết hạn mức hôm nay."
                     "\nChờ sang ngày mới, hoặc dùng Claude (đổi NHA_CUNG_CAP=claude).")

        return (f"Model '{self.st.model}' đã hết hạn mức MIỄN PHÍ của hôm nay{mo_ta_gioi_han}.\n\n"
                f"Chờ thêm trong hôm nay cũng không dùng được — đây là hạn mức theo NGÀY,\n"
                f"thường được cấp lại vào khoảng 14–15 giờ Việt Nam.\n\n"
                f"{goi_y}")

    @staticmethod
    def _boc_chi_tiet_han_muc(phan_hoi) -> dict:
        """Bóc quotaId, quotaValue và retryDelay ra khỏi phần details của lỗi 429."""
        kq: dict = {}
        try:
            details = phan_hoi.json().get("error", {}).get("details", []) or []
        except (ValueError, json.JSONDecodeError):
            return kq

        for d in details:
            loai = d.get("@type", "")
            if "QuotaFailure" in loai:
                vi_pham = (d.get("violations") or [{}])[0]
                kq["quota_id"] = vi_pham.get("quotaId", "")
                kq["gioi_han"] = vi_pham.get("quotaValue")
            elif "RetryInfo" in loai:
                khop = re.match(r"(\d+)", str(d.get("retryDelay", "")))
                if khop:
                    kq["cho_giay"] = int(khop.group(1))
        return kq

    def tim_model_con_han_muc(self) -> List[str]:
        """
        Thử từng model dự phòng bằng một yêu cầu cực ngắn để xem còn dùng được không.

        Mỗi lần thử tiêu tốn 1 lượt của model đó, nên chỉ gọi khi đã thực sự
        hết hạn mức — lúc đó thông tin này đáng giá hơn một lượt.
        """
        ket_qua = []
        for model in config.MODEL_DU_PHONG:
            if model == self.st.model:
                continue
            try:
                phan_hoi = requests.post(
                    f"{URL_GEMINI}/models/{model}:generateContent",
                    headers={"x-goog-api-key": self.st.api_key,
                             "Content-Type": "application/json"},
                    json={"contents": [{"parts": [{"text": "ok"}]}],
                          "generationConfig": {"maxOutputTokens": 5}},
                    timeout=25,
                )
                if phan_hoi.status_code == 200:
                    ket_qua.append(model)
            except Exception:  # noqa: BLE001 - chỉ là gợi ý, hỏng cũng không sao
                continue
        return ket_qua

    @staticmethod
    def _tim_model_thay_the(thong_diep: str) -> str:
        """
        Bóc tên model thay thế ra khỏi câu tiếng Anh Google trả về.
        Trả về chuỗi rỗng nếu không tìm thấy.
        """
        khop = re.search(r"use\s+models/([a-zA-Z0-9._-]+)", thong_diep)
        return khop.group(1) if khop else ""

    def liet_ke_model(self) -> List[str]:
        """Hỏi Google xem tài khoản này dùng được những model nào."""
        try:
            phan_hoi = requests.get(
                f"{URL_GEMINI}/models",
                headers={"x-goog-api-key": self.st.api_key},
                timeout=30,
            )
            if phan_hoi.status_code != 200:
                return []
            ket_qua = []
            for m in phan_hoi.json().get("models", []):
                # Chỉ lấy model sinh văn bản được
                if "generateContent" in (m.get("supportedGenerationMethods") or []):
                    ket_qua.append(m.get("name", "").replace("models/", ""))
            return ket_qua
        except Exception:  # noqa: BLE001 - chỉ là tiện ích phụ, hỏng cũng không sao
            return []


# =============================================================================
# ANTHROPIC CLAUDE
# =============================================================================

class NhaCungCapClaude:
    """
    Gọi Anthropic Claude qua thư viện chính thức.

    Thư viện `anthropic` chỉ được nạp KHI THỰC SỰ DÙNG, nên người chỉ xài
    Gemini không cần cài nó.
    """

    def __init__(self, st: Settings):
        self.st = st

    def viet_bai(self, prompt: str, nen_dung=None) -> KetQua:
        try:
            import anthropic
        except ImportError:
            raise LoiGoiAI(
                "Chưa cài thư viện cho Claude.\n\n"
                "Mở PowerShell và chạy:\n"
                "python -m pip install anthropic\n\n"
                "Hoặc đổi NHA_CUNG_CAP=gemini trong file .env để dùng bản miễn phí."
            ) from None

        client = anthropic.Anthropic(api_key=self.st.api_key, timeout=self.st.timeout)

        try:
            phan_hoi = client.messages.create(
                model=self.st.model,
                max_tokens=self.st.max_tokens,
                thinking={"type": "adaptive"},
                output_config={"effort": "medium"},
                messages=[{"role": "user", "content": prompt}],
            )
        except anthropic.AuthenticationError:
            raise LoiGoiAI(
                "API key của Claude không hợp lệ.\n"
                "Kiểm tra ANTHROPIC_API_KEY trong file .env."
            ) from None
        except anthropic.RateLimitError:
            raise LoiGoiAI("Đang bị giới hạn tốc độ. Chờ một lát rồi thử lại.") from None
        except anthropic.NotFoundError:
            raise LoiGoiAI(
                f"Không tìm thấy model '{self.st.model}'.\n"
                f"Sửa dòng CLAUDE_MODEL trong file .env thành claude-opus-5, "
                f"claude-sonnet-5 hoặc claude-haiku-4-5."
            ) from None
        except anthropic.APIStatusError as loi:
            raise LoiGoiAI(f"Claude báo lỗi {loi.status_code}: {loi.message}") from None
        except anthropic.APIConnectionError:
            raise LoiGoiAI("Không kết nối được tới Anthropic. Kiểm tra mạng.") from None

        if phan_hoi.stop_reason == "refusal":
            raise LoiGoiAI(
                "Claude từ chối viết nội dung này.\n"
                "Thử sửa lại prompt hoặc từ khóa cho trung tính hơn."
            )

        noi_dung = "".join(
            khoi.text for khoi in phan_hoi.content if khoi.type == "text"
        ).strip()

        if not noi_dung:
            raise LoiGoiAI("Claude trả về rỗng. Thử lại hoặc tăng MAX_TOKENS.")

        return KetQua(
            noi_dung=noi_dung,
            model=phan_hoi.model,
            token_vao=phan_hoi.usage.input_tokens,
            token_ra=phan_hoi.usage.output_tokens,
        )


# =============================================================================

def tao_nha_cung_cap(st: Settings):
    """Chọn lớp gọi API theo cấu hình NHA_CUNG_CAP trong .env."""
    if st.nha_cung_cap == "gemini":
        return NhaCungCapGemini(st)
    if st.nha_cung_cap == "claude":
        return NhaCungCapClaude(st)
    raise LoiGoiAI(f"Không hỗ trợ nhà cung cấp '{st.nha_cung_cap}'.")
