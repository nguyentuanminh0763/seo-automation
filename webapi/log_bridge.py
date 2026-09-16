# -*- coding: utf-8 -*-
"""
Đưa log của công cụ ra giao diện web.

VÌ SAO CẦN FILE NÀY?
    Ba công cụ đều dùng module logging của Python và in thẳng ra console. Giao
    diện web không đọc được console, nên phải bắt lấy từng dòng log ngay lúc nó
    sinh ra rồi đẩy sang trình duyệt.

    Cách làm giống hệt gui/log_bridge.py: gắn thêm một handler vào logger, thay
    vì in ra màn hình thì gọi hàm callback của việc đang chạy.

KHÁC MỘT CHỖ SO VỚI BẢN TKINTER:
    Bản tkinter chỉ có MỘT cửa sổ nên gắn handler vào logger là xong. Ở đây có
    thể mở nhiều tab trình duyệt, nên handler phải biết dòng log này thuộc việc
    nào. Giải pháp: mỗi việc gắn handler riêng của nó, và hai việc cùng loại
    không bao giờ được chạy song song (xem jobs.py) nên không lẫn log.
"""

import logging

# Tên logger của từng công cụ, khai đúng như trong trends/logger.py và
# suggest/logger.py. Thêm màn Viết bài sau thì thêm "writer": "writer".
TEN_LOGGER = {
    "trends": "trends",
    "suggest": "suggest",
}


class HandlerGoiHam(logging.Handler):
    """Handler của logging: thay vì in ra màn hình thì gọi một hàm."""

    def __init__(self, khi_co_log):
        super().__init__()
        self.khi_co_log = khi_co_log
        self.setFormatter(logging.Formatter(
            fmt="%(asctime)s  %(message)s",
            datefmt="%H:%M:%S",
        ))

    def emit(self, record: logging.LogRecord) -> None:
        try:
            self.khi_co_log(record.levelname, self.format(record))
        except Exception:  # noqa: BLE001 - log hỏng không được làm sập máy chủ
            pass


def gan(loai: str, khi_co_log) -> HandlerGoiHam:
    """
    Gắn handler vào logger của một công cụ. Trả về handler để gỡ ra sau.

    Cố ý KHÔNG dùng logging.basicConfig() như bản dòng lệnh: máy chủ web có thể
    được khởi động bằng pythonw.exe, lúc đó sys.stdout là None và StreamHandler
    sẽ ném lỗi ngay dòng log đầu tiên.
    """
    handler = HandlerGoiHam(khi_co_log)
    logger = logging.getLogger(TEN_LOGGER.get(loai, loai))
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.propagate = False   # không đẩy ngược lên logger gốc, tránh log trùng
    return handler


def go(loai: str, handler: HandlerGoiHam) -> None:
    """Gỡ handler sau khi việc chạy xong, tránh tích tụ qua nhiều lần chạy."""
    logging.getLogger(TEN_LOGGER.get(loai, loai)).removeHandler(handler)
