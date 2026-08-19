# -*- coding: utf-8 -*-
"""
Chạy công cụ thu thập ở luồng nền để cửa sổ không bị đơ.

Nếu chạy thẳng ở luồng chính, cửa sổ sẽ "Không phản hồi" suốt 13 phút và
người dùng tưởng ứng dụng bị treo.

QUY TẮC SỐNG CÒN VỚI TKINTER:
    Luồng nền TUYỆT ĐỐI không được gọi bất cứ hàm nào của tkinter, kể cả
    widget.after(). Bản đầu tiên làm vậy và sập ngay khi test:
        RuntimeError: main thread is not in main loop

    Nên luồng này chỉ CẤT kết quả vào chính nó. Luồng chính (trong tab_base.py)
    định kỳ kiểm tra xem luồng chạy xong chưa rồi mới đụng tới giao diện.
"""

import threading
import traceback
from typing import Callable, Optional

import pandas as pd


class LuongChay(threading.Thread):
    """
    Luồng nền thực thi một hàm thu thập.

    Tham số:
        ham_thu_thap : hàm nhận (nen_dung) và trả về DataFrame

    Đọc kết quả sau khi luồng kết thúc:
        .ket_qua : DataFrame nếu thành công, None nếu lỗi
        .loi     : chuỗi traceback nếu lỗi, None nếu thành công
    """

    def __init__(self, ham_thu_thap: Callable[[Callable[[], bool]], pd.DataFrame]):
        super().__init__(daemon=True)
        self.ham_thu_thap = ham_thu_thap
        self.ket_qua: Optional[pd.DataFrame] = None
        self.loi: Optional[str] = None          # traceback đầy đủ, để ghi log
        self.loi_goc: Optional[BaseException] = None   # đối tượng lỗi gốc
        self._co_dung = threading.Event()

    def yeu_cau_dung(self) -> None:
        """Bật cờ dừng. Công cụ sẽ thoát ở điểm kiểm tra gần nhất."""
        self._co_dung.set()

    def da_yeu_cau_dung(self) -> bool:
        """Hàm được truyền xuống công cụ để nó tự kiểm tra."""
        return self._co_dung.is_set()

    def run(self) -> None:
        try:
            self.ket_qua = self.ham_thu_thap(self.da_yeu_cau_dung)
        except Exception as loi:  # noqa: BLE001 - luồng nền chết âm thầm thì không ai biết
            # Giữ CẢ HAI: traceback để ghi log, và đối tượng lỗi để lấy nguyên
            # văn thông điệp. Bản đầu chỉ giữ traceback rồi cắt lấy dòng cuối,
            # làm mất sạch phần hướng dẫn nhiều dòng — đã gặp thật khi Google
            # báo tên model cần đổi mà hộp thoại chỉ hiện câu cuối cùng.
            self.loi = traceback.format_exc()
            self.loi_goc = loi
