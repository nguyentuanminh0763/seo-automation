# -*- coding: utf-8 -*-
"""
Tab Google Suggest — lấy từ khóa làm nội dung.
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, List

import pandas as pd

from suggest import Settings as SettingsSuggest
from suggest import config as config_suggest
from suggest import thu_thap, xuat_bao_cao

from .tab_base import TabCoSo


class TabSuggest(TabCoSo):
    ten_logger = "suggest"
    tieu_de = "Google Suggest — Từ khóa làm nội dung"
    mo_ta = ("Lấy hàng nghìn câu hỏi thật người dùng gõ vào Google. "
             "Chạy lâu hơn nhưng ra rất nhiều từ. Dùng để lên kế hoạch viết bài.")

    def __init__(self, cha):
        super().__init__(cha, config_suggest.SEED_KEYWORDS)

    def tao_bang_tuy_chon(self, cha) -> None:
        # --- Chế độ chạy nhanh ---
        self.bien_quick = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            cha, variable=self.bien_quick, command=self._cap_nhat_uoc_tinh,
            text="Chạy nhanh (bỏ quét bảng chữ cái a–z)",
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=2)

        # --- Định dạng file ---
        ttk.Label(cha, text="Xuất ra:").grid(row=1, column=0, sticky="w", pady=2)
        self.bien_dinh_dang = tk.StringVar(value="xlsx")
        khung = ttk.Frame(cha)
        khung.grid(row=1, column=1, sticky="w")
        ttk.Radiobutton(khung, text="Excel", variable=self.bien_dinh_dang,
                        value="xlsx").pack(side="left")
        ttk.Radiobutton(khung, text="CSV", variable=self.bien_dinh_dang,
                        value="csv").pack(side="left", padx=8)

        # --- Ước tính thời gian ---
        # Công cụ này chạy khá lâu nên phải báo trước, tránh người dùng tưởng bị treo.
        self.nhan_uoc_tinh = ttk.Label(cha, text="", foreground="#c60",
                                       font=("Segoe UI", 9, "italic"))
        self.nhan_uoc_tinh.grid(row=2, column=0, columnspan=2, sticky="w", pady=(6, 0))

        cha.columnconfigure(1, weight=1)
        self.after(200, self._cap_nhat_uoc_tinh)

    def _cap_nhat_uoc_tinh(self) -> None:
        """Tính lại thời gian dự kiến mỗi khi người dùng đổi tùy chọn."""
        try:
            so_seed = len(self.o_tu_khoa.lay_danh_sach())
        except Exception:  # noqa: BLE001 - lúc khởi tạo ô nhập có thể chưa sẵn sàng
            return

        st = self._lay_settings()
        so_luot = so_seed * st.so_bien_the_moi_seed()
        so_phut = so_luot * (st.delay_min + st.delay_max) / 2 / 60

        self.nhan_uoc_tinh.configure(
            text=f"≈ {so_luot:,} lượt hỏi Google · dự kiến {so_phut:.0f} phút"
        )

    def _lay_settings(self) -> SettingsSuggest:
        return SettingsSuggest(
            dung_bang_chu_cai=(config_suggest.DUNG_BANG_CHU_CAI and not self.bien_quick.get()),
            output_format=self.bien_dinh_dang.get(),
        )

    def tao_ham_thu_thap(self, seeds: List[str]) -> Callable:
        st = self._lay_settings()
        return lambda nen_dung: thu_thap(seeds, st, nen_dung=nen_dung)

    def xuat_file(self, df: pd.DataFrame) -> str:
        return xuat_bao_cao(df, self._lay_settings())
