# -*- coding: utf-8 -*-
"""
Kiểm tra bài viết theo chuẩn SEO — ĐẾM BẰNG CODE, KHÔNG HỎI AI.

VÌ SAO FILE NÀY TỒN TẠI
    Prompt ban đầu yêu cầu AI tự làm bảng tự kiểm tra ở cuối bài. Đo thực tế
    trên một bài viết cho thấy AI khai 3.682 từ / 17 lần từ khóa / 18 thẻ H3,
    trong khi số thật là 5.876 từ / 26 lần / 29 thẻ — sai 50–60%.

    Mô hình ngôn ngữ không đếm được. Nó sinh ra bảng trông rất thuyết phục với
    con số bịa, và người đọc thấy "Đạt" hết nên yên tâm đăng bài chưa đạt chuẩn.
    Tệ hơn, khi được yêu cầu "tự sửa nếu chưa đạt", nó có động cơ tự chấm mình
    đạt để khỏi phải viết lại.

    Đếm bằng code mất một phần nghìn giây và luôn đúng.

RANH GIỚI
    Một số tiêu chí không đếm được bằng máy — chất lượng E-E-A-T, câu văn có
    gượng không. Những mục đó trả về trạng thái CAN_NGUOI_KIEM chứ không giả vờ
    chấm điểm. Bảng kiểm tra nói dối thì tệ hơn không có bảng.
"""

import re
import unicodedata
from dataclasses import dataclass, field
from typing import List, Optional

from . import config

DAT = "dat"
CHUA_DAT = "chua_dat"
CAN_NGUOI_KIEM = "can_nguoi_kiem"
KHONG_AP_DUNG = "khong_ap_dung"


@dataclass
class KetQuaKiemTra:
    """Một dòng trong bảng kiểm tra."""

    ten: str
    chuan: str
    thuc_te: str
    trang_thai: str
    goi_y: str = ""

    @property
    def bieu_tuong(self) -> str:
        return {
            DAT: "✅",
            CHUA_DAT: "❌",
            CAN_NGUOI_KIEM: "👁",
            KHONG_AP_DUNG: "—",
        }.get(self.trang_thai, "?")


@dataclass
class BaoCaoKiemTra:
    """Toàn bộ kết quả kiểm tra một bài viết."""

    cac_muc: List[KetQuaKiemTra] = field(default_factory=list)
    # Nói rõ phần nào của văn bản được đem đếm. Nếu bài có khối metadata và
    # bảng tự kiểm tra, chỉ phần thân bài mới được tính — không nói ra thì
    # người dùng sửa chữ ở ngoài phạm vi đó rồi thắc mắc sao số không đổi.
    pham_vi_dem: str = ""

    @property
    def so_dat(self) -> int:
        return sum(1 for m in self.cac_muc if m.trang_thai == DAT)

    @property
    def so_chua_dat(self) -> int:
        return sum(1 for m in self.cac_muc if m.trang_thai == CHUA_DAT)

    @property
    def so_can_kiem(self) -> int:
        return sum(1 for m in self.cac_muc if m.trang_thai == CAN_NGUOI_KIEM)

    @property
    def so_cham_duoc(self) -> int:
        """Số mục máy chấm được — mẫu số thật của tỷ lệ đạt."""
        return sum(1 for m in self.cac_muc
                   if m.trang_thai in (DAT, CHUA_DAT))

    def tom_tat(self) -> str:
        if self.so_chua_dat == 0:
            return f"✅ Đạt {self.so_dat}/{self.so_cham_duoc} tiêu chí máy chấm được"
        return f"⚠ {self.so_chua_dat} tiêu chí chưa đạt (trên {self.so_cham_duoc} mục chấm được)"


# =============================================================================
# HÀM CHÍNH
# =============================================================================

def kiem_tra(noi_dung: str, tu_khoa: str) -> BaoCaoKiemTra:
    """Chạy toàn bộ kiểm tra trên nội dung Markdown."""
    than_bai, pham_vi = _lay_than_bai(noi_dung)
    meta = _boc_metadata(noi_dung)

    bao_cao = BaoCaoKiemTra(pham_vi_dem=pham_vi)
    them = bao_cao.cac_muc.append
    C = config.CHUAN_SEO

    # --- 1. Độ dài ---
    so_tu = dem_tu(than_bai)
    them(_khoang(
        "1. Tổng số từ", so_tu, C["so_tu_toi_thieu"], C["so_tu_toi_da"],
        f"{C['so_tu_toi_thieu']:,}–{C['so_tu_toi_da']:,}", f"{so_tu:,} từ",
        "Bài ngắn hơn chuẩn — bổ sung mục còn thiếu."
        if so_tu < C["so_tu_toi_thieu"] else
        "Bài dài hơn chuẩn — cắt phần lặp ý, đừng để dài mà loãng.",
    ))

    # --- 2-3. Cấu trúc heading ---
    h1s = re.findall(r"^# (.+)$", than_bai, re.M)
    h2s = re.findall(r"^## (.+)$", than_bai, re.M)
    h3s = re.findall(r"^### (.+)$", than_bai, re.M)

    them(KetQuaKiemTra(
        "2. Số thẻ H1", f"= {C['so_h1']}", f"{len(h1s)} thẻ",
        DAT if len(h1s) == C["so_h1"] else CHUA_DAT,
        "" if len(h1s) == C["so_h1"] else
        ("Nhiều H1 thường do AI dùng # cho tiêu đề các PHẦN. "
         "Yêu cầu prompt ngăn cách bằng --- thay vì #."),
    ))
    them(KetQuaKiemTra(
        "3. Số thẻ H2 / H3", f"H2 ≥ {C['so_h2_toi_thieu']}",
        f"{len(h2s)} H2 / {len(h3s)} H3",
        DAT if len(h2s) >= C["so_h2_toi_thieu"] else CHUA_DAT,
        "" if len(h2s) >= C["so_h2_toi_thieu"] else "Thiếu mục — xem lại danh sách H2 bắt buộc.",
    ))

    # --- 4. Mật độ từ khóa ---
    # Chấm trên CỤM LÕI chứ không phải nguyên câu hỏi: với "cpu hàng tray là gì",
    # lặp nguyên cụm 15-20 lần là bất khả thi, còn lõi "cpu hàng tray" thì tự
    # nhiên. Đo thật trên một bài: nguyên cụm 12 lần, cụm lõi 38 lần.
    loi = lay_tu_khoa_loi(tu_khoa)
    so_lan = dem_tu_khoa(than_bai, loi)
    mat_do = (so_lan / so_tu * 100) if so_tu else 0.0
    ghi_chu_loi = "" if loi == tu_khoa.strip() else f" (cụm lõi \"{loi}\")"
    them(_khoang(
        f"4. Số lần từ khóa{ghi_chu_loi}", so_lan, C["tu_khoa_min"], C["tu_khoa_max"],
        f"{C['tu_khoa_min']}–{C['tu_khoa_max']} lần", f"{so_lan} lần",
        "Thiếu — rải thêm ở phần thân bài."
        if so_lan < C["tu_khoa_min"] else
        "Thừa — bỏ bớt, thay bằng 'lỗi này', 'hiện tượng trên'.",
    ))
    them(_khoang(
        "   Mật độ từ khóa", mat_do, C["mat_do_min"], C["mat_do_max"],
        f"{C['mat_do_min']:.2f}–{C['mat_do_max']:.2f}%", f"{mat_do:.2f}%",
        "Mật độ lệch chuẩn — điều chỉnh cùng số lần xuất hiện.",
    ))

    # --- 5. Vị trí từ khóa ---
    them(_co_khong("5a. Từ khóa trong H1",
                   any(_chua(h, loi) for h in h1s),
                   "Sửa lại H1 cho chứa từ khóa chính."))
    dau_bai = " ".join(_bo_markup(than_bai).split()[:100])
    them(_co_khong("5b. Từ khóa trong 100 từ đầu", _chua(dau_bai, loi),
                   "Đưa từ khóa vào đoạn mở bài."))
    h2_co_kw = sum(1 for h in h2s if _chua(h, loi))
    them(KetQuaKiemTra(
        "5c. Từ khóa trong H2", f"≥ {C['h2_chua_tu_khoa_min']} thẻ", f"{h2_co_kw} thẻ",
        DAT if h2_co_kw >= C["h2_chua_tu_khoa_min"] else CHUA_DAT,
        "" if h2_co_kw >= C["h2_chua_tu_khoa_min"] else "Thêm từ khóa vào vài H2 — nhưng đừng nhét vào tất cả.",
    ))
    them(_co_khong("5d. Từ khóa trong kết bài",
                   _chua(" ".join(_bo_markup(than_bai).split()[-200:]), loi),
                   "Nhắc lại từ khóa ở đoạn kết."))

    # --- 6-7. Metadata ---
    them(_do_dai("6. Độ dài SEO Title", meta.get("title"),
                 0, C["title_toi_da"], f"≤ {C['title_toi_da']} ký tự",
                 "Rút ngắn title, Google cắt phần thừa."))
    them(_do_dai("7. Độ dài Meta Description", meta.get("meta"),
                 C["meta_min"], C["meta_max"],
                 f"{C['meta_min']}–{C['meta_max']} ký tự",
                 "Viết lại meta cho đúng độ dài."))
    them(_co_khong("   Có slug đề xuất", bool(meta.get("slug")),
                   "Prompt cần yêu cầu xuất slug.", khong_co_thi=KHONG_AP_DUNG))

    # --- 8. Liên kết ---
    internal, external = dem_link(noi_dung)
    them(_khoang("8. Internal link", len(internal), C["internal_min"], C["internal_max"],
                 f"{C['internal_min']}–{C['internal_max']}", f"{len(internal)} link",
                 "Chèn thêm link nội bộ vào đoạn liên quan."
                 if len(internal) < C["internal_min"] else "Bớt link nội bộ cho tự nhiên."))
    them(_khoang("   External link", len(external), C["external_min"], C["external_max"],
                 f"{C['external_min']}–{C['external_max']}", f"{len(external)} link",
                 "Thiếu link nguồn uy tín — đây là tín hiệu Authoritativeness."
                 if len(external) < C["external_min"] else "Nhiều link ra ngoài quá."))

    # --- 9-12. Các khối bắt buộc ---
    so_anh = len(re.findall(config.DAU_HIEU["anh"], noi_dung))
    them(KetQuaKiemTra(
        "9. Số ảnh đánh dấu", f"≥ {C['so_anh_toi_thieu']}", f"{so_anh} ảnh",
        DAT if so_anh >= C["so_anh_toi_thieu"] else CHUA_DAT,
        "" if so_anh >= C["so_anh_toi_thieu"] else "Thêm vị trí ảnh — ảnh tự chụp tại tiệm là lợi thế thật.",
    ))
    them(_co_khong("10. Block Trả lời nhanh",
                   _tim(noi_dung, config.DAU_HIEU["tra_loi_nhanh"]),
                   "Thiếu khối tối ưu featured snippet."))

    so_faq = _dem_faq(noi_dung)
    them(KetQuaKiemTra(
        "11. Số câu FAQ", f"≥ {C['so_faq_toi_thieu']}", f"{so_faq} câu",
        DAT if so_faq >= C["so_faq_toi_thieu"] else CHUA_DAT,
        "" if so_faq >= C["so_faq_toi_thieu"] else "Thêm câu hỏi người dùng hay tìm.",
    ))
    them(_co_khong("12. Checklist cho người đọc",
                   _tim(noi_dung, config.DAU_HIEU["checklist"]),
                   "Thiếu mục checklist tự kiểm tra."))

    # --- 13. E-E-A-T: chỉ kiểm được phần có dấu hiệu máy thấy ---
    # Bài về khái niệm hay so sánh không có thao tác phần cứng thì không cần
    # cảnh báo an toàn. Máy không phân biệt được, nên để người đọc tự quyết.
    co_canh_bao = _tim(noi_dung, config.DAU_HIEU["canh_bao_an_toan"])
    them(KetQuaKiemTra(
        "13a. Cảnh báo an toàn (Trust)", "có nếu bài có thao tác máy",
        "có" if co_canh_bao else "không có",
        DAT if co_canh_bao else CAN_NGUOI_KIEM,
        "" if co_canh_bao else
        "Bài có hướng dẫn tháo lắp/cắm điện thì phải có cảnh báo. "
        "Bài thuần lý thuyết thì bỏ qua mục này.",
    ))
    them(_co_khong("13b. Nêu giới hạn nội dung (Trust)",
                   _tim(noi_dung, config.DAU_HIEU["gioi_han"]),
                   "Thiếu câu nêu rõ giới hạn / khi nào không nên tự làm."))
    them(KetQuaKiemTra(
        "13c. Chất lượng Experience", "2 chi tiết nghề",
        "máy không chấm được", CAN_NGUOI_KIEM,
        "Tự đọc: có chi tiết nào chỉ người làm nghề mới biết không?",
    ))

    # --- 14. NAP / tác giả / ngày ---
    them(_co_khong("14a. Có NAP (hotline)",
                   any(n in noi_dung for n in config.NAP_CAN_CO),
                   "Thiếu số hotline."))
    them(_co_khong("14b. Có author bio",
                   _tim(noi_dung, config.DAU_HIEU["author_bio"]),
                   "Thiếu khối giới thiệu đội ngũ."))

    ngay = _tim_ngay(noi_dung)
    co_cho_trong = "[NGÀY ĐĂNG]" in noi_dung
    them(KetQuaKiemTra(
        "14c. Ngày cập nhật", "chỗ trống để bạn điền",
        "[NGÀY ĐĂNG] — điền tay" if co_cho_trong else (ngay or "không thấy"),
        DAT if co_cho_trong else (CAN_NGUOI_KIEM if ngay else CHUA_DAT),
        "" if co_cho_trong else
        ("AI đoán ngày sẽ ra ngày sai lệch nhiều năm — đã gặp bài ghi 24/10/2023. "
         "Sửa tay trước khi đăng."
         if ngay else "Thiếu ngày cập nhật — thêm vào đầu hoặc cuối bài."),
    ))

    # --- 15. Nhồi từ khóa ---
    cau_nhoi = tim_cau_nhoi_tu_khoa(than_bai, loi)
    them(KetQuaKiemTra(
        "15. Câu lặp từ khóa ≥2 lần", "0 câu", f"{len(cau_nhoi)} câu",
        DAT if not cau_nhoi else CHUA_DAT,
        "" if not cau_nhoi else "Xem danh sách bên dưới và viết lại các câu đó.",
    ))

    # --- Bịa số liệu: cảnh báo riêng vì đây là rủi ro E-E-A-T lớn nhất ---
    so_bia = tim_so_lieu_nghi_bia(than_bai)
    them(KetQuaKiemTra(
        "16. Số liệu có thể bị bịa", "0 chỗ", f"{len(so_bia)} chỗ",
        DAT if not so_bia else CHUA_DAT,
        "" if not so_bia else
        "AI hay bịa phần trăm dù prompt đã cấm. Kiểm tra từng chỗ, "
        "xóa hoặc thay bằng số liệu thật của cửa hàng.",
    ))

    return bao_cao


# =============================================================================
# ĐẾM
# =============================================================================

def dem_tu(noi_dung: str) -> int:
    """Đếm âm tiết cách nhau bởi dấu cách, bỏ markup và bảng."""
    return len([t for t in _bo_markup(noi_dung).split() if t.strip()])


def dem_tu_khoa(noi_dung: str, tu_khoa: str) -> int:
    """Đếm số lần từ khóa xuất hiện, không phân biệt hoa thường và dấu."""
    if not tu_khoa.strip():
        return 0
    return len(re.findall(re.escape(_chuan_hoa(tu_khoa)), _chuan_hoa(noi_dung)))


# Những chữ biến một danh từ thành câu hỏi. Bỏ chúng đi sẽ còn lại phần lõi —
# thứ thực sự được lặp lại tự nhiên trong bài.
_DAU_CAU_HOI = [
    "cach", "huong dan", "tai sao", "co nen", "so sanh", "review", "top",
    "mua", "noi ban", "dia chi ban", "lam sao", "lam the nao",
]
_DUOI_CAU_HOI = [
    "la gi", "gia bao nhieu", "bao nhieu", "loai nao tot", "o dau",
    "nhu the nao", "ra sao", "co tot khong", "khong", "tot nhat", "nen mua",
]


def lay_tu_khoa_loi(tu_khoa: str) -> str:
    """
    Bóc phần lõi của từ khóa bằng cách bỏ các chữ dùng để hỏi.

    VÌ SAO CẦN
        Với từ khóa "cpu hàng tray là gì", đếm nguyên cụm chỉ ra 12 lần trong khi
        cụm lõi "cpu hàng tray" xuất hiện 38 lần. Lặp nguyên câu hỏi 15–20 lần là
        bất khả thi và đọc lên rất gượng — Google cũng không đòi hỏi vậy. Phần lõi
        mới là thứ đáng đếm.

    Trả về chính từ khóa gốc nếu bóc xong không còn gì đáng kể.
    """
    tu = tu_khoa.strip().split()
    if not tu:
        return tu_khoa

    # Cắt theo SỐ TỪ trên danh sách đã tách, để chữ trả về vẫn còn nguyên dấu.
    for dau in sorted(_DAU_CAU_HOI, key=lambda x: -len(x.split())):
        n = len(dau.split())
        if len(tu) > n and _chuan_hoa(" ".join(tu[:n])) == dau:
            tu = tu[n:]
            break
    for duoi in sorted(_DUOI_CAU_HOI, key=lambda x: -len(x.split())):
        n = len(duoi.split())
        if len(tu) > n and _chuan_hoa(" ".join(tu[-n:])) == duoi:
            tu = tu[:-n]
            break

    # Bóc quá tay, còn lại một chữ trơ trọi thì giữ nguyên từ khóa gốc.
    return " ".join(tu) if len(tu) >= 2 else tu_khoa.strip()


def dem_link(noi_dung: str):
    """Tách link nội bộ và link ra ngoài. Trả về (internal, external), đã bỏ trùng."""
    tat_ca = re.findall(r"https?://[^\s\)\]\">]+", noi_dung)
    internal = {u for u in tat_ca if config.TEN_MIEN in u}
    external = {u for u in tat_ca if config.TEN_MIEN not in u}
    return sorted(internal), sorted(external)


def tim_cau_nhoi_tu_khoa(noi_dung: str, tu_khoa: str) -> List[str]:
    """
    Tìm câu chứa từ khóa từ 2 lần trở lên — dấu hiệu nhồi nhét rõ nhất
    mà máy phát hiện được.
    """
    if not tu_khoa.strip():
        return []
    kq = []
    for cau in re.split(r"(?<=[.!?…])\s+|\n", _bo_markup(noi_dung)):
        if dem_tu_khoa(cau, tu_khoa) >= 2:
            kq.append(cau.strip())
    return kq


def tim_so_lieu_nghi_bia(noi_dung: str) -> List[str]:
    """
    Tìm câu chứa phần trăm hoặc 'X ca / X trường hợp' — những con số AI hay
    bịa ra để nghe thuyết phục.

    Không khẳng định là bịa; chỉ nêu ra để người viết đối chiếu với số liệu
    thật của cửa hàng. Bỏ qua phần bàn về mật độ từ khóa của chính bài.
    """
    kq = []
    for cau in re.split(r"(?<=[.!?…])\s+|\n", _bo_markup(noi_dung)):
        if not re.search(r"\d{1,3}\s?%|\b\d{2,4}\s+(ca|trường hợp|khách|lượt)\b", cau, re.I):
            continue
        if re.search(r"mật độ|từ khóa|SEO Title|Meta", cau, re.I):
            continue        # câu đang bàn về chính bài viết, không phải số liệu
        if _la_cach_noi_quen(cau):
            continue
        kq.append(cau.strip())
    return kq


# "mới 100%", "cam kết 100% chính hãng" là cách nói quen của ngành bán lẻ VN,
# không phải số liệu thống kê. Bản đầu bắt nhầm 5/5 câu kiểu này nên phải lọc.
_CACH_NOI_QUEN = re.compile(
    r"(mới|nguyên|chính hãng|cam kết|đảm bảo|bảo đảm|hoàn toàn|zin)\s*100\s?%"
    r"|100\s?%\s*(chính hãng|mới|nguyên|zin|new)",
    re.I,
)


def _la_cach_noi_quen(cau: str) -> bool:
    """Câu chỉ chứa '100%' theo lối nói quen thì bỏ qua, không coi là số liệu."""
    if _CACH_NOI_QUEN.search(cau):
        # Vẫn báo nếu trong câu còn phần trăm KHÁC 100 — đó mới là số đáng ngờ.
        return not re.search(r"\b(?!100\b)\d{1,3}\s?%", cau)
    return False


# =============================================================================
# TIỆN ÍCH NỘI BỘ
# =============================================================================

def _lay_than_bai(noi_dung: str):
    """
    Lấy phần bài viết thật, bỏ khối metadata và bảng tự kiểm tra nếu có.

    Quan trọng: đếm cả hai phần đó sẽ thổi phồng số từ và số lần từ khóa —
    đúng lỗi mà bản đầu tiên mắc phải.

    Trả về (thân_bài, mô_tả_phạm_vi). Phần mô tả được hiện lên giao diện để
    người dùng biết chữ mình vừa sửa có nằm trong vùng đếm hay không.
    """
    # Chấp nhận cả "# PHẦN 2", "**PHẦN 2**" và "PHẦN 2" trần.
    # Prompt mới cố tình KHÔNG dùng # cho các mốc này, vì dùng # thì WordPress
    # hiểu thành thẻ H1 và bài có 3-4 H1 thay vì 1.
    moc = r"^[#*\s]*PHẦN\s*{n}\b.*$"
    bat_dau = re.search(moc.format(n=2), noi_dung, re.M | re.I)
    ket_thuc = re.search(moc.format(n=3), noi_dung, re.M | re.I)
    dau = bat_dau.end() if bat_dau else 0
    cuoi = ket_thuc.start() if ket_thuc else len(noi_dung)
    than = noi_dung[dau:cuoi].strip()

    if not than:
        return noi_dung, "toàn bộ văn bản"
    if bat_dau and ket_thuc:
        return than, "chỉ phần thân bài (giữa PHẦN 2 và PHẦN 3)"
    if bat_dau:
        return than, "từ PHẦN 2 trở đi"
    if ket_thuc:
        return than, "phần trước PHẦN 3"
    return than, "toàn bộ văn bản"


def _boc_metadata(noi_dung: str) -> dict:
    """Bóc slug / title / meta ra khỏi khối PHẦN 1 nếu prompt có yêu cầu."""
    def lay(nhan: str) -> Optional[str]:
        m = re.search(rf"{nhan}[^:：\n]*[:：]\s*(.+)", noi_dung, re.I)
        if not m:
            return None
        gia_tri = m.group(1).strip()
        gia_tri = re.sub(r"\s*[—\-–]\s*\d+\s*ký tự.*$", "", gia_tri)
        return gia_tri.strip("*`\"' ") or None

    return {"slug": lay("slug"), "title": lay("SEO Title"), "meta": lay("Meta Description")}


def _bo_markup(t: str) -> str:
    t = re.sub(r"^\|.*\|$", " ", t, flags=re.M)     # bảng
    t = re.sub(r"<[^>]+>", " ", t)                  # thẻ HTML
    t = re.sub(r"\[ẢNH[^\]]*\]", " ", t)            # đánh dấu ảnh
    t = re.sub(r"https?://\S+", " ", t)             # URL
    t = re.sub(r"[#*_`>\[\]()]", " ", t)
    return t


def _chuan_hoa(t: str) -> str:
    """
    Bỏ dấu và chuyển thường, để 'Máy Tính' khớp với 'máy tính'.

    Phải xử lý riêng chữ đ: NFD tách được dấu của â, ê, ô... nhưng KHÔNG tách
    được đ (U+0111 là một ký tự riêng, không phải d + dấu gạch). Bỏ sót chỗ này
    khiến "ở đâu" chuẩn hóa thành "o đau" chứ không phải "o dau" — đã làm hỏng
    việc bóc cụm lõi của từ khóa "laptop cũ ở đâu".
    """
    t = t.lower().replace("đ", "d")
    t = unicodedata.normalize("NFD", t)
    return "".join(c for c in t if unicodedata.category(c) != "Mn")


def _chua(chuoi: str, tu_khoa: str) -> bool:
    return bool(tu_khoa.strip()) and _chuan_hoa(tu_khoa) in _chuan_hoa(chuoi)


def _tim(noi_dung: str, mau: str) -> bool:
    return bool(re.search(mau, noi_dung, re.I | re.M))


def _dem_faq(noi_dung: str) -> int:
    """Đếm heading dạng câu hỏi trong khu vực FAQ."""
    m = re.search(config.DAU_HIEU["faq"], noi_dung, re.I | re.M)
    if not m:
        return 0
    khu = noi_dung[m.end():]
    ket = re.search(r"^##\s", khu, re.M)
    if ket:
        khu = khu[:ket.start()]
    return len(re.findall(r"^#{3,4}\s+.+", khu, re.M))


def _tim_ngay(noi_dung: str) -> Optional[str]:
    m = re.search(r"cập nhật[^\n]{0,20}?(\d{1,2}[/-]\d{1,2}[/-]\d{4})", noi_dung, re.I)
    return m.group(1) if m else None


def _khoang(ten, gia_tri, thap, cao, chuan, thuc_te, goi_y) -> KetQuaKiemTra:
    ok = thap <= gia_tri <= cao
    return KetQuaKiemTra(ten, chuan, thuc_te, DAT if ok else CHUA_DAT, "" if ok else goi_y)


def _do_dai(ten, chuoi, thap, cao, chuan, goi_y) -> KetQuaKiemTra:
    if chuoi is None:
        return KetQuaKiemTra(ten, chuan, "không có trong bài", KHONG_AP_DUNG,
                             "Prompt này không yêu cầu xuất khối metadata.")
    n = len(chuoi)
    ok = thap <= n <= cao
    return KetQuaKiemTra(ten, chuan, f"{n} ký tự", DAT if ok else CHUA_DAT, "" if ok else goi_y)


def _co_khong(ten, co, goi_y, khong_co_thi=CHUA_DAT) -> KetQuaKiemTra:
    return KetQuaKiemTra(ten, "có", "có" if co else "không có",
                         DAT if co else khong_co_thi, "" if co else goi_y)
