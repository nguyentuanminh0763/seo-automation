# -*- coding: utf-8 -*-
"""
Tab Google Trends — dò từ khóa đột biến (Breakout).
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, List

import pandas as pd

from trends import Settings as SettingsTrends
from trends import config as config_trends
from trends import quet_breakout, xuat_bao_cao

from .tab_base import TabCoSo


class TabTrends(TabCoSo):
    ten_logger = "trends"
    tieu_de = "Google Trends — Từ khóa đột biến"
    mo_ta = ("Tìm từ khóa đang TĂNG VỌT (trên 5.000%) trong 30 ngày qua. "
             "Chạy nhanh, ra ít từ. Dùng để bắt trend và canh nhập hàng.")

    def __init__(self, cha):
        super().__init__(cha, config_trends.SEED_KEYWORDS)

    def tao_bang_tuy_chon(self, cha) -> None:
        # --- Khung thời gian ---
        ttk.Label(cha, text="Khung thời gian:").grid(row=0, column=0, sticky="w", pady=2)
        self.bien_timeframe = tk.StringVar(value=config_trends.TIMEFRAME)
        ttk.Combobox(
            cha, textvariable=self.bien_timeframe, state="readonly", width=16,
            values=["now 7-d", "today 1-m", "today 3-m", "today 12-m"],
        ).grid(row=0, column=1, sticky="ew", pady=2)

        # --- Khu vực ---
        ttk.Label(cha, text="Khu vực:").grid(row=1, column=0, sticky="w", pady=2)
        self.bien_geo = tk.StringVar(value=config_trends.GEO)
        ttk.Combobox(
            cha, textvariable=self.bien_geo, state="readonly", width=16,
            values=["VN", "VN-SG", "VN-HN"],
        ).grid(row=1, column=1, sticky="ew", pady=2)

        # --- Lấy thêm Rising ---
        self.bien_rising = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            cha, variable=self.bien_rising,
            text=f"Lấy thêm từ tăng ≥ {config_trends.RISING_THRESHOLD}% (nhiều kết quả hơn)",
        ).grid(row=2, column=0, columnspan=2, sticky="w", pady=(6, 2))

        # --- Định dạng file ---
        ttk.Label(cha, text="Xuất ra:").grid(row=3, column=0, sticky="w", pady=2)
        self.bien_dinh_dang = tk.StringVar(value="xlsx")
        khung = ttk.Frame(cha)
        khung.grid(row=3, column=1, sticky="w")
        ttk.Radiobutton(khung, text="Excel", variable=self.bien_dinh_dang,
                        value="xlsx").pack(side="left")
        ttk.Radiobutton(khung, text="CSV", variable=self.bien_dinh_dang,
                        value="csv").pack(side="left", padx=8)

        cha.columnconfigure(1, weight=1)

    def _lay_settings(self) -> SettingsTrends:
        return SettingsTrends(
            geo=self.bien_geo.get(),
            timeframe=self.bien_timeframe.get(),
            include_rising=self.bien_rising.get(),
            output_format=self.bien_dinh_dang.get(),
        )

    def tao_ham_thu_thap(self, seeds: List[str]) -> Callable:
        st = self._lay_settings()
        return lambda nen_dung: quet_breakout(seeds, st, nen_dung=nen_dung)

    def xuat_file(self, df: pd.DataFrame) -> str:
        return xuat_bao_cao(df, self._lay_settings())
