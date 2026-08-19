# -*- coding: utf-8 -*-
"""
Log cho công cụ viết bài.

Giống hai công cụ kia: console Windows dùng cp1252 nên phải ép UTF-8,
không thì log tiếng Việt vỡ hết.

⚠ TUYỆT ĐỐI không log nội dung file .env hay API key.
"""

import logging
import sys


def thiet_lap_log(muc: int = logging.INFO) -> None:
    """Gọi một lần ở đầu chương trình khi chạy bằng dòng lệnh."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    logging.basicConfig(
        level=muc,
        format="%(asctime)s | %(levelname)-7s | %(message)s",
        datefmt="%H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def lay_log(ten: str = "writer") -> logging.Logger:
    """Lấy logger dùng chung cho các module."""
    return logging.getLogger(ten)
