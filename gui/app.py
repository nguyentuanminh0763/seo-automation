# -*- coding: utf-8 -*-
"""
Cửa sổ chính của ứng dụng.
"""

import tkinter as tk
from tkinter import messagebox, ttk

from .tab_suggest import TabSuggest
from .tab_trends import TabTrends

TIEU_DE = "SEO Keyword Tools — giaphongpc.vn"
KICH_THUOC_MAC_DINH = "1180x760"
KICH_THUOC_TOI_THIEU = (960, 640)


class UngDung(tk.Tk):
    """Cửa sổ chính gồm hai tab, mỗi tab một công cụ."""

    def __init__(self):
        super().__init__()

        self.title(TIEU_DE)
        self.geometry(KICH_THUOC_MAC_DINH)
        self.minsize(*KICH_THUOC_TOI_THIEU)

        self._dat_giao_dien()
        self._dung_tab()

        # Hỏi lại trước khi tắt nếu đang chạy dở, tránh mất công chạy 13 phút.
        self.protocol("WM_DELETE_WINDOW", self._khi_dong_cua_so)

    def _dat_giao_dien(self) -> None:
        """Dùng theme 'vista' cho giống ứng dụng Windows thật."""
        style = ttk.Style(self)
        for ten in ("vista", "winnative", "clam"):
            if ten in style.theme_names():
                style.theme_use(ten)
                break

    def _dung_tab(self) -> None:
        so_tay = ttk.Notebook(self)
        so_tay.pack(fill="both", expand=True, padx=8, pady=8)

        self.tab_suggest = TabSuggest(so_tay)
        self.tab_trends = TabTrends(so_tay)

        # Suggest đặt trước vì đây là công cụ dùng thường xuyên hơn.
        so_tay.add(self.tab_suggest, text="  Từ khóa làm nội dung  ")
        so_tay.add(self.tab_trends, text="  Từ khóa đột biến  ")

    def _dang_chay(self) -> bool:
        return any(
            tab.luong is not None and tab.luong.is_alive()
            for tab in (self.tab_suggest, self.tab_trends)
        )

    def _khi_dong_cua_so(self) -> None:
        if self._dang_chay():
            dong_y = messagebox.askyesno(
                "Đang chạy dở",
                "Công cụ đang chạy. Tắt bây giờ sẽ mất toàn bộ kết quả chưa lưu.\n\n"
                "Bạn có chắc muốn tắt không?",
            )
            if not dong_y:
                return
        self.destroy()


def chay() -> None:
    """Điểm khởi động ứng dụng."""
    UngDung().mainloop()
