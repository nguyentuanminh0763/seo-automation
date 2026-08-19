# -*- coding: utf-8 -*-
"""
Đọc file .env — nơi cất API key.

Cố ý TỰ VIẾT thay vì cài thư viện python-dotenv: chỉ mất khoảng 30 dòng,
mà giữ được nguyên tắc của dự án là hạn chế tối đa thư viện ngoài.

⚠ File .env chứa API key và đã bị chặn trong .gitignore.
   Tuyệt đối không in nội dung file này ra log.
"""

import os
from typing import Dict

TEN_FILE = ".env"
TEN_FILE_MAU = ".env.example"


def doc_env(thu_muc_goc: str) -> Dict[str, str]:
    """
    Đọc file .env ở thư mục gốc dự án, trả về dict.

    Bỏ qua dòng trống và dòng chú thích bắt đầu bằng #.
    Nếu không có file .env, trả về dict rỗng (không ném lỗi) — phần kiểm tra
    thiếu key để cho settings.py lo, vì nó biết cần key nào.
    """
    duong_dan = os.path.join(thu_muc_goc, TEN_FILE)
    ket_qua: Dict[str, str] = {}

    if not os.path.exists(duong_dan):
        return ket_qua

    with open(duong_dan, "r", encoding="utf-8") as f:
        for dong in f:
            dong = dong.strip()
            if not dong or dong.startswith("#") or "=" not in dong:
                continue
            khoa, _, gia_tri = dong.partition("=")
            ket_qua[khoa.strip()] = _bo_dau_nhay(gia_tri.strip())

    return ket_qua


def _bo_dau_nhay(gia_tri: str) -> str:
    """Bỏ dấu nháy bao quanh nếu người dùng gõ KEY="abc" thay vì KEY=abc."""
    if len(gia_tri) >= 2 and gia_tri[0] == gia_tri[-1] and gia_tri[0] in "\"'":
        return gia_tri[1:-1]
    return gia_tri


def thieu_file_env(thu_muc_goc: str) -> bool:
    """Kiểm tra người dùng đã tạo file .env chưa."""
    return not os.path.exists(os.path.join(thu_muc_goc, TEN_FILE))


def huong_dan_tao_env(thu_muc_goc: str) -> str:
    """Câu hướng dẫn hiện lên giao diện khi chưa có file .env."""
    return (
        f"Chưa có file {TEN_FILE}.\n\n"
        f"Cách tạo:\n"
        f"1. Vào thư mục {thu_muc_goc}\n"
        f"2. Copy file {TEN_FILE_MAU}, đổi tên bản copy thành {TEN_FILE}\n"
        f"3. Mở bằng Notepad, dán API key vào\n\n"
        f"Lấy key Gemini miễn phí tại: https://aistudio.google.com"
    )
