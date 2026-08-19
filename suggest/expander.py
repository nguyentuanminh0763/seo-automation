# -*- coding: utf-8 -*-
"""
Sinh ra các biến thể truy vấn từ MỘT từ khóa gốc.

Đây là "công thức" của dân SEO: không hỏi Google mỗi từ gốc một lần,
mà ghép thêm từ mồi và bảng chữ cái để moi ra càng nhiều câu hỏi thật càng tốt.

Ví dụ với từ gốc "máy tính":
    máy tính                 (hỏi trần)
    cách máy tính            (ghép trước)
    tại sao máy tính         (ghép trước)
    máy tính là gì           (ghép sau)
    máy tính giá bao nhiêu   (ghép sau)
    máy tính a, máy tính b   (bảng chữ cái)
"""

from typing import List

from .settings import Settings


def sinh_bien_the(seed: str, st: Settings) -> List[str]:
    """
    Tạo danh sách truy vấn sẽ gửi cho Google, từ một từ khóa gốc.

    Trả về danh sách đã bỏ trùng, giữ nguyên thứ tự.
    """
    seed = seed.strip()
    if not seed:
        return []

    bien_the: List[str] = [seed]

    # 1. Ghép từ mồi vào TRƯỚC: "cách" + "máy tính" -> "cách máy tính"
    bien_the += [f"{tu_moi} {seed}" for tu_moi in st.tu_moi_truoc]

    # 2. Ghép từ mồi vào SAU: "máy tính" + "là gì" -> "máy tính là gì"
    bien_the += [f"{seed} {tu_moi}" for tu_moi in st.tu_moi_sau]

    # 3. Ghép từng chữ cái: "máy tính a", "máy tính b"...
    #    Mẹo kinh điển giúp moi ra những cụm mà ta không tự nghĩ tới được.
    if st.dung_bang_chu_cai:
        bien_the += [f"{seed} {chu}" for chu in st.bang_chu_cai]

    return _bo_trung(bien_the)


def _bo_trung(danh_sach: List[str]) -> List[str]:
    """Bỏ phần tử trùng nhưng GIỮ NGUYÊN thứ tự xuất hiện."""
    da_thay = set()
    ket_qua = []
    for phan_tu in danh_sach:
        khoa = phan_tu.lower()
        if khoa not in da_thay:
            da_thay.add(khoa)
            ket_qua.append(phan_tu)
    return ket_qua
