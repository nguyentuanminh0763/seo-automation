# -*- coding: utf-8 -*-
"""
Các thành phần giao diện dùng chung cho cả hai tab.
"""

import logging
import tkinter as tk
from tkinter import ttk
from typing import List

import pandas as pd

# Hiển thị tối đa ngần này dòng trong bảng. File Excel vẫn có đủ toàn bộ.
# Đổ 7.000 dòng vào bảng làm giao diện khựng vài giây nên phải giới hạn.
SO_DONG_HIEN_TOI_DA = 1000


class HopLog(ttk.Frame):
    """Ô hiển thị tiến trình chạy, tự cuộn xuống dòng mới nhất."""

    def __init__(self, cha, **kw):
        super().__init__(cha, **kw)

        self.o_text = tk.Text(self, height=12, wrap="none", state="disabled",
                              font=("Consolas", 9), background="#1e1e1e",
                              foreground="#d4d4d4", insertbackground="#d4d4d4")
        thanh_cuon = ttk.Scrollbar(self, orient="vertical", command=self.o_text.yview)
        self.o_text.configure(yscrollcommand=thanh_cuon.set)

        self.o_text.grid(row=0, column=0, sticky="nsew")
        thanh_cuon.grid(row=0, column=1, sticky="ns")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Tô màu theo mức độ để lỗi nổi bật lên giữa hàng trăm dòng log.
        self.o_text.tag_configure("canh_bao", foreground="#dcdcaa")
        self.o_text.tag_configure("loi", foreground="#f48771")

    def them_dong(self, muc: int, noi_dung: str) -> None:
        the = ""
        if muc >= logging.ERROR:
            the = "loi"
        elif muc >= logging.WARNING:
            the = "canh_bao"

        self.o_text.configure(state="normal")
        self.o_text.insert("end", noi_dung + "\n", the)
        self.o_text.see("end")          # tự cuộn xuống dòng mới nhất
        self.o_text.configure(state="disabled")

    def xoa_sach(self) -> None:
        self.o_text.configure(state="normal")
        self.o_text.delete("1.0", "end")
        self.o_text.configure(state="disabled")


class BangKetQua(ttk.Frame):
    """Bảng hiển thị kết quả, có ô lọc nhanh ở trên."""

    def __init__(self, cha, **kw):
        super().__init__(cha, **kw)

        self._df = pd.DataFrame()

        # --- Thanh lọc ---
        thanh_loc = ttk.Frame(self)
        thanh_loc.grid(row=0, column=0, sticky="ew", pady=(0, 4))
        ttk.Label(thanh_loc, text="Lọc nhanh:").pack(side="left")
        self.bien_loc = tk.StringVar()
        self.bien_loc.trace_add("write", lambda *_: self._ve_lai())
        ttk.Entry(thanh_loc, textvariable=self.bien_loc, width=34).pack(side="left", padx=6)
        self.nhan_dem = ttk.Label(thanh_loc, text="")
        self.nhan_dem.pack(side="left", padx=10)

        # --- Bảng ---
        self.bang = ttk.Treeview(self, show="headings", height=12)
        cuon_doc = ttk.Scrollbar(self, orient="vertical", command=self.bang.yview)
        cuon_ngang = ttk.Scrollbar(self, orient="horizontal", command=self.bang.xview)
        self.bang.configure(yscrollcommand=cuon_doc.set, xscrollcommand=cuon_ngang.set)

        self.bang.grid(row=1, column=0, sticky="nsew")
        cuon_doc.grid(row=1, column=1, sticky="ns")
        cuon_ngang.grid(row=2, column=0, sticky="ew")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

    def nap_du_lieu(self, df: pd.DataFrame) -> None:
        """Nạp DataFrame mới vào bảng."""
        self._df = df if df is not None else pd.DataFrame()
        self._dung_cot(list(self._df.columns))
        self._ve_lai()

    def _dung_cot(self, cac_cot: List[str]) -> None:
        """Dựng lại tiêu đề cột. Mỗi công cụ có bộ cột khác nhau."""
        self.bang["columns"] = cac_cot
        for ten_cot in cac_cot:
            self.bang.heading(ten_cot, text=ten_cot)
            # Cột từ khóa cần rộng, các cột còn lại hẹp cho đỡ chiếm chỗ.
            rong = 300 if "eyword" in ten_cot else 130
            self.bang.column(ten_cot, width=rong, anchor="w", stretch=False)

    def _ve_lai(self) -> None:
        """Vẽ lại bảng theo từ khóa lọc hiện tại."""
        self.bang.delete(*self.bang.get_children())

        if self._df.empty:
            self.nhan_dem.configure(text="")
            return

        df = self._df
        tu_loc = self.bien_loc.get().strip().lower()
        if tu_loc:
            # Lọc trên toàn bộ các cột, không chỉ cột đầu.
            mat_na = df.astype(str).apply(
                lambda cot: cot.str.lower().str.contains(tu_loc, regex=False)
            ).any(axis=1)
            df = df[mat_na]

        for _, dong in df.head(SO_DONG_HIEN_TOI_DA).iterrows():
            self.bang.insert("", "end", values=[str(g) for g in dong.tolist()])

        if len(df) > SO_DONG_HIEN_TOI_DA:
            self.nhan_dem.configure(
                text=f"Hiện {SO_DONG_HIEN_TOI_DA}/{len(df)} dòng — file Excel có đủ"
            )
        else:
            self.nhan_dem.configure(text=f"{len(df)} dòng")


class ONhapTuKhoa(ttk.Frame):
    """Ô nhập từ khóa gốc, mỗi dòng một từ."""

    def __init__(self, cha, danh_sach_mac_dinh: List[str], **kw):
        super().__init__(cha, **kw)

        self.o_text = tk.Text(self, height=10, width=32, wrap="none", font=("Segoe UI", 10))
        thanh_cuon = ttk.Scrollbar(self, orient="vertical", command=self.o_text.yview)
        self.o_text.configure(yscrollcommand=thanh_cuon.set)

        self.o_text.grid(row=0, column=0, sticky="nsew")
        thanh_cuon.grid(row=0, column=1, sticky="ns")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.dat_danh_sach(danh_sach_mac_dinh)

    def lay_danh_sach(self) -> List[str]:
        """Đọc nội dung, mỗi dòng thành một từ khóa. Bỏ dòng trống."""
        noi_dung = self.o_text.get("1.0", "end")
        return [dong.strip() for dong in noi_dung.splitlines() if dong.strip()]

    def dat_danh_sach(self, danh_sach: List[str]) -> None:
        self.o_text.delete("1.0", "end")
        self.o_text.insert("1.0", "\n".join(danh_sach))
