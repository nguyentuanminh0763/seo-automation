# -*- coding: utf-8 -*-
"""
Quản lý "việc" — một lần chạy công cụ ở luồng nền.

VÌ SAO KHÔNG CHẠY THẲNG TRONG YÊU CẦU HTTP?
    Một lần chạy Suggest mất khoảng 13 phút. Trình duyệt và mọi proxy đều tự cắt
    kết nối trước đó rất lâu. Nên yêu cầu HTTP chỉ TẠO việc rồi trả về ngay một
    mã số; trình duyệt dùng mã đó để mở một kênh riêng nghe tiến trình.

QUY TẮC KẾ THỪA TỪ gui/worker.py:
    Luồng nền không được gọi thẳng vào tầng giao diện. Ở đây "giao diện" là kết
    nối HTTP của trình duyệt. Luồng nền chỉ đẩy sự kiện vào hàng đợi; luồng phục
    vụ kết nối tự lấy ra mà gửi đi. Nhờ vậy trình duyệt đóng tab giữa chừng cũng
    không làm việc đang chạy bị ảnh hưởng.

CHỈ MỘT VIỆC THU THẬP TẠI MỘT THỜI ĐIỂM:
    Trends và Suggest dùng chung một khóa. Chạy song song nghĩa là gấp đôi số
    lần hỏi Google từ cùng một địa chỉ IP — đúng thứ CLAUDE_RULES.md cấm.

    Màn Viết bài (làm sau) phải có khóa RIÊNG, vì nó gọi OpenAI/Gemini chứ
    không gọi Google — bắt nó chờ Suggest chạy xong 13 phút là vô lý.
"""

import threading
import time
import traceback
import uuid
from collections import OrderedDict
from typing import Callable, Dict, List, Optional

from . import config, log_bridge

# Trạng thái của một việc
CHO = "cho"                  # vừa tạo, luồng chưa kịp chạy
DANG_CHAY = "dang_chay"
XONG = "xong"
DA_DUNG = "da_dung"          # người dùng bấm Dừng, vẫn giữ kết quả thu được
LOI = "loi"

# Việc nào dùng chung khóa nào. Cùng tên khóa = không chạy song song được.
KHOA_CUA_LOAI = {
    "trends": "thu_thap",
    "suggest": "thu_thap",
}


class DangBan(Exception):
    """Ném ra khi đã có việc cùng nhóm đang chạy. routes.py đổi thành lỗi 409."""


class Viec:
    """Một lần chạy công cụ. Đối tượng này sống trong bộ nhớ máy chủ."""

    def __init__(self, loai: str, mo_ta: str = ""):
        self.id = uuid.uuid4().hex[:12]
        self.loai = loai
        self.mo_ta = mo_ta
        self.trang_thai = CHO
        self.bat_dau = time.time()
        self.ket_thuc: Optional[float] = None

        # Kết quả đã đổi sang JSON, trình duyệt đọc trực tiếp.
        self.ket_qua: Optional[dict] = None
        # Dữ liệu thô giữ lại cho việc xuất file (DataFrame, BaiViet...).
        # Cố ý tách khỏi ket_qua vì DataFrame không đổi sang JSON gọn được.
        self.du_lieu_tho = None
        self.loi: Optional[str] = None
        self.loi_chi_tiet: Optional[str] = None

        self._co_dung = threading.Event()
        self._khoa = threading.Lock()
        # Lịch sử sự kiện để tab mở muộn (hoặc tải lại trang) vẫn xem được
        # những gì đã xảy ra, thay vì nhìn một ô log trống trơn.
        self._lich_su: List[dict] = []
        self._nguoi_nghe: List["object"] = []   # hàng đợi của từng kết nối SSE
        self._so_thu_tu = 0

    # --- Dừng giữa chừng ---------------------------------------------------

    def yeu_cau_dung(self) -> None:
        """Bật cờ dừng. Công cụ sẽ thoát ở điểm kiểm tra gần nhất."""
        self._co_dung.set()

    def da_yeu_cau_dung(self) -> bool:
        """Hàm truyền xuống công cụ để nó tự kiểm tra giữa các bước."""
        return self._co_dung.is_set()

    # --- Sự kiện -----------------------------------------------------------

    def phat(self, su_kien: dict) -> None:
        """
        Gửi một sự kiện tới mọi kết nối đang nghe, đồng thời lưu vào lịch sử.

        Gọi được từ luồng nền vì mọi thứ đụng tới đều nằm sau khóa.
        """
        with self._khoa:
            self._so_thu_tu += 1
            su_kien = dict(su_kien, stt=self._so_thu_tu)

            # Chỉ log mới bị cắt bớt. Sự kiện trạng thái/kết quả phải giữ đủ,
            # không thì tab mở muộn sẽ không biết việc đã xong hay chưa.
            self._lich_su.append(su_kien)
            if len(self._lich_su) > config.SO_DONG_LOG_GIU:
                self._cat_bot_lich_su()

            nguoi_nghe = list(self._nguoi_nghe)

        for hang_doi in nguoi_nghe:
            try:
                hang_doi.put_nowait(su_kien)
            except Exception:  # noqa: BLE001 - một kết nối hỏng không được ảnh hưởng việc chạy
                pass

    def _cat_bot_lich_su(self) -> None:
        """Bỏ bớt dòng log cũ nhất, giữ nguyên các sự kiện quan trọng."""
        quan_trong = [sk for sk in self._lich_su if sk.get("loai") != "log"]
        cac_log = [sk for sk in self._lich_su if sk.get("loai") == "log"]
        con_lai = max(config.SO_DONG_LOG_GIU - len(quan_trong), 100)
        cac_log = cac_log[-con_lai:]
        self._lich_su = sorted(quan_trong + cac_log, key=lambda sk: sk["stt"])

    def ghi_log(self, muc: str, chu: str) -> None:
        """Đẩy một dòng log ra giao diện."""
        self.phat({"loai": "log", "muc": muc, "chu": chu})

    def dang_ky_nghe(self, hang_doi) -> List[dict]:
        """
        Một kết nối SSE mới vào nghe. Trả về lịch sử để phát lại trước.

        Nhờ phát lại này mà tải lại trang giữa chừng vẫn thấy nguyên tiến trình
        đã chạy, thay vì một ô log trống trơn.
        """
        with self._khoa:
            self._nguoi_nghe.append(hang_doi)
            return list(self._lich_su)

    def huy_nghe(self, hang_doi) -> None:
        with self._khoa:
            if hang_doi in self._nguoi_nghe:
                self._nguoi_nghe.remove(hang_doi)

    # --- Tóm tắt cho API ---------------------------------------------------

    def tom_tat(self) -> dict:
        """Ảnh chụp trạng thái hiện tại, dùng cho GET /api/viec/<id>."""
        return {
            "id": self.id,
            "loai": self.loai,
            "mo_ta": self.mo_ta,
            "trang_thai": self.trang_thai,
            "giay_da_chay": round((self.ket_thuc or time.time()) - self.bat_dau, 1),
            "ket_qua": self.ket_qua,
            "loi": self.loi,
        }


class QuanLyViec:
    """Kho chứa mọi việc đang và đã chạy trong phiên làm việc này."""

    def __init__(self):
        self._cac_viec: "OrderedDict[str, Viec]" = OrderedDict()
        self._khoa = threading.Lock()
        self._dang_chay: Dict[str, str] = {}   # tên khóa -> id việc đang giữ

    def lay(self, ma: str) -> Optional[Viec]:
        with self._khoa:
            return self._cac_viec.get(ma)

    def danh_sach(self) -> List[dict]:
        with self._khoa:
            return [v.tom_tat() for v in reversed(self._cac_viec.values())]

    def dang_ban(self, loai: str) -> Optional[Viec]:
        """Trả về việc đang chiếm khóa của nhóm này, None nếu đang rảnh."""
        ten_khoa = KHOA_CUA_LOAI.get(loai, loai)
        with self._khoa:
            ma = self._dang_chay.get(ten_khoa)
            viec = self._cac_viec.get(ma) if ma else None
        if viec and viec.trang_thai in (CHO, DANG_CHAY):
            return viec
        return None

    def tao_va_chay(self, loai: str, mo_ta: str,
                    cong_viec: Callable[[Viec], dict]) -> Viec:
        """
        Tạo việc mới và chạy `cong_viec(viec)` ở luồng nền.

        `cong_viec` trả về dict kết quả đã sẵn sàng đổi sang JSON, hoặc ném lỗi.
        Ném DangBan nếu nhóm này đang có việc chạy dở.
        """
        dang_ban = self.dang_ban(loai)
        if dang_ban is not None:
            raise DangBan(dang_ban.id)

        viec = Viec(loai, mo_ta)
        ten_khoa = KHOA_CUA_LOAI.get(loai, loai)

        with self._khoa:
            self._cac_viec[viec.id] = viec
            self._dang_chay[ten_khoa] = viec.id
            self._don_viec_cu()

        threading.Thread(target=self._chay, args=(viec, cong_viec),
                         daemon=True).start()
        return viec

    def _don_viec_cu(self) -> None:
        """Bỏ việc cũ nhất khi vượt hạn mức. Gọi khi đang giữ khóa."""
        while len(self._cac_viec) > config.SO_VIEC_GIU:
            ma, viec = next(iter(self._cac_viec.items()))
            if viec.trang_thai in (CHO, DANG_CHAY):
                break          # không bao giờ dọn việc đang chạy
            self._cac_viec.pop(ma)

    def _chay(self, viec: Viec, cong_viec: Callable[[Viec], dict]) -> None:
        """Thân luồng nền. Mọi lỗi đều bị bắt — luồng chết âm thầm thì không ai biết."""
        handler = log_bridge.gan(viec.loai, viec.ghi_log)
        viec.trang_thai = DANG_CHAY
        viec.phat({"loai": "trang_thai", "trang_thai": DANG_CHAY})

        try:
            viec.ket_qua = cong_viec(viec)
            viec.trang_thai = DA_DUNG if viec.da_yeu_cau_dung() else XONG
        except Exception as loi:  # noqa: BLE001 - chốt chặn cuối cùng
            # Giữ CẢ HAI như gui/worker.py: nguyên văn thông điệp để hiện lên
            # giao diện, và traceback để soi khi cần. Bản đầu của giao diện
            # tkinter chỉ giữ traceback rồi cắt lấy dòng cuối, làm mất sạch
            # phần hướng dẫn nhiều dòng mà Google trả về.
            viec.trang_thai = LOI
            viec.loi = str(loi) or loi.__class__.__name__
            viec.loi_chi_tiet = traceback.format_exc()
        finally:
            viec.ket_thuc = time.time()
            log_bridge.go(viec.loai, handler)
            ten_khoa = KHOA_CUA_LOAI.get(viec.loai, viec.loai)
            with self._khoa:
                if self._dang_chay.get(ten_khoa) == viec.id:
                    self._dang_chay.pop(ten_khoa, None)

        if viec.trang_thai == LOI:
            viec.phat({"loai": "loi", "chu": viec.loi})
        else:
            viec.phat({"loai": "xong",
                       "trang_thai": viec.trang_thai,
                       "ket_qua": viec.ket_qua,
                       "giay": round(viec.ket_thuc - viec.bat_dau, 1)})


# Một kho duy nhất dùng chung cho cả máy chủ.
kho = QuanLyViec()
