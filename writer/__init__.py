# -*- coding: utf-8 -*-
"""
Package viết bài chuẩn SEO bằng AI, cho giaphongpc.vn.

KHÁC GÌ HAI PACKAGE KIA?
    trends/   "Cái gì đang nóng lên?"      -> bắt trend
    suggest/  "Người ta hay hỏi gì?"       -> lấy từ khóa
    writer/   "Viết bài từ từ khóa đó"     -> ra nội dung đăng web

BẢN ĐỒ CÁC FILE:

    config.py     Hằng số. LƯU Ý: API key KHÔNG nằm ở đây mà ở file .env
                  ngoài thư mục gốc, vì .env không bị đẩy lên GitHub.
    env.py        Đọc file .env (tự viết, không cần thư viện ngoài).
    settings.py   Gói cấu hình + kiểm tra thiếu key, báo lỗi dễ hiểu.
    logger.py     Log, ép UTF-8 cho console Windows.
    prompts.py    Nạp file prompt NGƯỜI DÙNG tự viết trong thư mục prompts/.
    providers.py  Gọi API Gemini hoặc Claude. Thêm AI mới thì sửa file này.
    formatter.py  Markdown -> HTML sạch cho WordPress.
    clipboard.py  Ghi clipboard KÈM ĐỊNH DẠNG (giống copy từ ChatGPT).
    generator.py  Điều phối: ghép prompt -> gọi AI -> HTML -> lưu file.

NGUYÊN TẮC:
    Nội dung prompt là của người dùng. Package này không hiểu, không sửa,
    không áp đặt gì lên prompt — chỉ thay {keyword} và nối ghi chú vào cuối.
"""

from .generator import BaiViet, luu_bai, viet_bai
from .logger import lay_log, thiet_lap_log
from .prompts import Prompt, liet_ke_prompt
from .providers import LoiGoiAI
from .settings import Settings, ThieuCauHinh

__all__ = [
    "BaiViet", "viet_bai", "luu_bai",
    "Prompt", "liet_ke_prompt",
    "Settings", "ThieuCauHinh", "LoiGoiAI",
    "thiet_lap_log", "lay_log",
]
__version__ = "1.0.0"
