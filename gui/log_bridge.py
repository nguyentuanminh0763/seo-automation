# -*- coding: utf-8 -*-
"""
Cầu nối đưa log từ luồng chạy nền lên ô hiển thị của giao diện.

VÌ SAO CẦN FILE NÀY?
    Tkinter chỉ cho phép cập nhật giao diện từ luồng chính. Công cụ thu thập lại
    chạy ở luồng nền (để cửa sổ không bị đơ). Nếu luồng nền ghi thẳng lên giao diện
    thì ứng dụng sẽ treo hoặc crash.

    Giải pháp: luồng nền đẩy dòng log vào một hàng đợi (queue), luồng chính định kỳ
    lấy ra và hiển thị. Đây là cách chuẩn để hai luồng nói chuyện an toàn.
"""

import logging
import queue


class HangDoiLogHandler(logging.Handler):
    """Handler của logging, thay vì in ra màn hình thì đẩy vào hàng đợi."""

    def __init__(self, hang_doi: "queue.Queue[str]"):
        super().__init__()
        self.hang_doi = hang_doi
        self.setFormatter(logging.Formatter(
            fmt="%(asctime)s  %(message)s",
            datefmt="%H:%M:%S",
        ))

    def emit(self, record: logging.LogRecord) -> None:
        try:
            self.hang_doi.put((record.levelno, self.format(record)))
        except Exception:  # noqa: BLE001 - log hỏng không được làm sập ứng dụng
            pass


def gan_vao_logger(hang_doi: "queue.Queue[str]", ten_logger: str) -> HangDoiLogHandler:
    """
    Gắn handler vào một logger cụ thể ('trends' hoặc 'suggest').

    Cố ý KHÔNG dùng logging.basicConfig() như bản dòng lệnh, vì khi chạy bằng
    pythonw.exe thì sys.stdout là None, StreamHandler sẽ lỗi khi ghi.
    """
    handler = HangDoiLogHandler(hang_doi)
    logger = logging.getLogger(ten_logger)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.propagate = False   # không đẩy ngược lên logger gốc, tránh log trùng
    return handler


def go_khoi_logger(handler: HangDoiLogHandler, ten_logger: str) -> None:
    """Gỡ handler sau khi chạy xong, tránh tích tụ handler qua nhiều lần chạy."""
    logging.getLogger(ten_logger).removeHandler(handler)
