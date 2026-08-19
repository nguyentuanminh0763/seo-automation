# -*- coding: utf-8 -*-
"""
Thiết lập log cho công cụ Suggest.

LƯU Ý SỐNG CÒN TRÊN WINDOWS:
    Console Windows mặc định dùng bảng mã cp1252, KHÔNG hiển thị được tiếng Việt có dấu.
    Nếu không ép stdout sang UTF-8, mọi dòng log tiếng Việt sẽ ném UnicodeEncodeError
    và làm vỡ toàn bộ output.
"""

import logging
import sys


def thiet_lap_log(muc: int = logging.INFO) -> None:
    """Gọi 1 lần duy nhất ở đầu main(), trước khi làm bất cứ việc gì khác."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    logging.basicConfig(
        level=muc,
        format="%(asctime)s | %(levelname)-7s | %(message)s",
        datefmt="%H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def lay_log(ten: str = "suggest") -> logging.Logger:
    """Lấy logger dùng chung cho các module."""
    return logging.getLogger(ten)
