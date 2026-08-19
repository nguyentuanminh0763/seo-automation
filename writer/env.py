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


def ghi_env(thu_muc_goc: str, cap_nhat: Dict[str, str]) -> None:
    """
    Cập nhật các khóa trong .env, GIỮ NGUYÊN chú thích và thứ tự dòng.

    Viết đè cả file sẽ xóa sạch phần hướng dẫn mà người dùng cần đọc lại sau
    này, nên hàm này chỉ thay đúng phần giá trị của những dòng cần sửa.
    Khóa chưa có trong file thì thêm vào cuối.
    """
    duong_dan = os.path.join(thu_muc_goc, TEN_FILE)
    con_lai = dict(cap_nhat)
    cac_dong = []

    if os.path.exists(duong_dan):
        with open(duong_dan, "r", encoding="utf-8") as f:
            cac_dong = f.read().splitlines()

    for i, dong in enumerate(cac_dong):
        tach = dong.strip()
        if not tach or tach.startswith("#") or "=" not in tach:
            continue
        khoa = tach.split("=", 1)[0].strip()
        if khoa in con_lai:
            cac_dong[i] = f"{khoa}={con_lai.pop(khoa)}"

    if con_lai:
        cac_dong.append("")
        cac_dong.append("# --- Thêm tự động từ màn hình Cấu hình AI ---")
        cac_dong += [f"{k}={v}" for k, v in con_lai.items()]

    # Ghi ra file tạm rồi mới thay thế: nếu máy tắt giữa chừng, file .env cũ
    # vẫn nguyên vẹn thay vì mất sạch API key.
    tam = duong_dan + ".tmp"
    with open(tam, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(cac_dong).rstrip() + "\n")
    os.replace(tam, duong_dan)


def tao_env_tu_mau(thu_muc_goc: str) -> bool:
    """Chưa có .env thì tạo từ .env.example. Trả về True nếu vừa tạo."""
    dich = os.path.join(thu_muc_goc, TEN_FILE)
    if os.path.exists(dich):
        return False
    nguon = os.path.join(thu_muc_goc, TEN_FILE_MAU)
    noi_dung = ""
    if os.path.exists(nguon):
        with open(nguon, "r", encoding="utf-8") as f:
            noi_dung = f.read()
    with open(dich, "w", encoding="utf-8", newline="\n") as f:
        f.write(noi_dung)
    return True


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
