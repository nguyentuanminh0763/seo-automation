# -*- coding: utf-8 -*-
"""
Phân loại keyword theo Ý ĐỊNH TÌM KIẾM và đề xuất loại bài nên viết.

Đây là phần biến một danh sách keyword thô thành KẾ HOẠCH NỘI DUNG dùng được ngay:
biết từ nào viết bài hướng dẫn, từ nào làm trang bán hàng.
"""

from typing import Tuple

from . import config
from .settings import Settings


def phan_loai(keyword: str) -> Tuple[str, str]:
    """
    Đọc keyword, trả về (nhóm_ý_định, loại_bài_đề_xuất).

    Cách hoạt động: duyệt LUAT_PHAN_LOAI trong config.py theo đúng thứ tự,
    gặp nhóm nào có dấu hiệu khớp trước thì lấy nhóm đó.
    Vì vậy thứ tự trong config.py chính là thứ tự ưu tiên.
    """
    kw = f" {keyword.lower().strip()} "  # thêm khoảng trắng 2 đầu để khớp " vs " chính xác

    for nhom, loai_bai, cac_dau_hieu in config.LUAT_PHAN_LOAI:
        if any(dau_hieu in kw for dau_hieu in cac_dau_hieu):
            return nhom, loai_bai

    return config.NHOM_MAC_DINH


def la_keyword_rac(keyword: str, st: Settings) -> bool:
    """
    Kiểm tra keyword có nên bị loại bỏ không.

    Loại bỏ khi:
        - Quá ngắn (ít hơn DO_DAI_TOI_THIEU từ) -> quá chung chung, không viết bài được
        - Chứa từ ngoài ngành (tiktok, iphone, shopee...) -> nhiễu, không liên quan
    """
    kw = keyword.lower().strip()

    if len(kw.split()) < st.do_dai_toi_thieu:
        return True

    return any(tu_loai in kw for tu_loai in st.tu_khoa_loai_bo)


def uu_tien_content(nhom: str) -> int:
    """
    Chấm điểm ưu tiên để sắp xếp báo cáo (số nhỏ = nên làm trước).

    Ưu tiên nhóm dễ lên top và kéo traffic tốt: lỗi và khái niệm là hai nhóm
    người dùng tìm nhiều, đối thủ ít đầu tư, dễ xếp hạng nhất.
    """
    thu_tu = {
        "Khắc phục lỗi": 1,
        "Khái niệm": 2,
        "Hướng dẫn": 3,
        "So sánh - Tư vấn": 4,
        "Thương mại": 5,
        "Thông tin sản phẩm": 6,
    }
    return thu_tu.get(nhom, 9)
