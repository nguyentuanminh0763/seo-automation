# -*- coding: utf-8 -*-
"""
Khung chung cho cả hai tab.

Hai tab giống nhau tới 80%: đều có ô nhập từ khóa, nút chạy, ô log, bảng kết quả.
Chỉ khác ở phần tùy chọn riêng và hàm thu thập được gọi. Nên phần chung gom vào đây,
mỗi tab con chỉ cần khai báo phần khác biệt.
"""

import os
import queue
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable, List, Optional

import pandas as pd

from .log_bridge import gan_vao_logger, go_khoi_logger
from .widgets import BangKetQua, HopLog, ONhapTuKhoa
from .worker import LuongChay

CHU_KY_DOC_LOG_MS = 120   # cứ 120ms lại lấy log mới từ hàng đợi ra hiển thị


class TabCoSo(ttk.Frame):
    """Lớp cha cho tab Trends và tab Suggest."""

    # --- Tab con phải khai báo lại 3 thuộc tính này ---
    ten_logger = ""        # 'trends' hoặc 'suggest'
    tieu_de = ""
    mo_ta = ""

    def __init__(self, cha, seeds_mac_dinh: List[str]):
        super().__init__(cha, padding=10)

        self.hang_doi_log: "queue.Queue" = queue.Queue()
        self.luong: Optional[LuongChay] = None
        self.handler_log = None
        self.duong_dan_file: Optional[str] = None

        self._dung_giao_dien(seeds_mac_dinh)
        self._doc_hang_doi_log()

    # =========================================================================
    # DỰNG GIAO DIỆN
    # =========================================================================

    def _dung_giao_dien(self, seeds_mac_dinh: List[str]) -> None:
        ttk.Label(self, text=self.tieu_de, font=("Segoe UI", 13, "bold")).grid(
            row=0, column=0, columnspan=2, sticky="w")
        ttk.Label(self, text=self.mo_ta, foreground="#555").grid(
            row=1, column=0, columnspan=2, sticky="w", pady=(0, 10))

        # --- CỘT TRÁI: nhập liệu và tùy chọn ---
        cot_trai = ttk.Frame(self)
        cot_trai.grid(row=2, column=0, sticky="nsew", padx=(0, 12))

        ttk.Label(cot_trai, text="Từ khóa gốc (mỗi dòng một từ):",
                  font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.o_tu_khoa = ONhapTuKhoa(cot_trai, seeds_mac_dinh)
        self.o_tu_khoa.pack(fill="both", expand=True, pady=(4, 8))

        khung_tuy_chon = ttk.LabelFrame(cot_trai, text="Tùy chọn", padding=8)
        khung_tuy_chon.pack(fill="x", pady=(0, 8))
        self.tao_bang_tuy_chon(khung_tuy_chon)

        # --- Nút bấm ---
        khung_nut = ttk.Frame(cot_trai)
        khung_nut.pack(fill="x")
        self.nut_chay = ttk.Button(khung_nut, text="▶  Bắt đầu chạy", command=self._bat_dau)
        self.nut_chay.pack(fill="x", pady=2)
        self.nut_dung = ttk.Button(khung_nut, text="■  Dừng lại",
                                   command=self._dung, state="disabled")
        self.nut_dung.pack(fill="x", pady=2)

        # --- CỘT PHẢI: log và kết quả ---
        cot_phai = ttk.Frame(self)
        cot_phai.grid(row=2, column=1, sticky="nsew")

        ttk.Label(cot_phai, text="Tiến trình chạy:",
                  font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.hop_log = HopLog(cot_phai)
        self.hop_log.pack(fill="both", expand=True, pady=(4, 8))

        ttk.Label(cot_phai, text="Kết quả:",
                  font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.bang_ket_qua = BangKetQua(cot_phai)
        self.bang_ket_qua.pack(fill="both", expand=True, pady=(4, 8))

        # --- Thanh trạng thái dưới cùng ---
        thanh_duoi = ttk.Frame(cot_phai)
        thanh_duoi.pack(fill="x")
        self.nhan_trang_thai = ttk.Label(thanh_duoi, text="Sẵn sàng.", foreground="#0a7")
        self.nhan_trang_thai.pack(side="left")
        self.nut_mo_file = ttk.Button(thanh_duoi, text="Mở file Excel",
                                      command=self._mo_file, state="disabled")
        self.nut_mo_file.pack(side="right", padx=4)
        ttk.Button(thanh_duoi, text="Mở thư mục kết quả",
                   command=self._mo_thu_muc).pack(side="right")

        self.columnconfigure(1, weight=3)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

    # =========================================================================
    # TAB CON PHẢI CÀI ĐẶT LẠI 3 HÀM NÀY
    # =========================================================================

    def tao_bang_tuy_chon(self, cha) -> None:
        """Dựng các ô tùy chọn riêng của từng công cụ."""
        raise NotImplementedError

    def tao_ham_thu_thap(self, seeds: List[str]) -> Callable:
        """Trả về hàm nhận (nen_dung) và trả về DataFrame."""
        raise NotImplementedError

    def xuat_file(self, df: pd.DataFrame) -> str:
        """Ghi DataFrame ra file, trả về đường dẫn."""
        raise NotImplementedError

    # =========================================================================
    # CHẠY VÀ DỪNG
    # =========================================================================

    def _bat_dau(self) -> None:
        seeds = self.o_tu_khoa.lay_danh_sach()
        if not seeds:
            messagebox.showwarning("Thiếu từ khóa",
                                   "Hãy nhập ít nhất một từ khóa gốc.")
            return

        self.hop_log.xoa_sach()
        self.bang_ket_qua.nap_du_lieu(pd.DataFrame())
        self.duong_dan_file = None
        self.nut_mo_file.configure(state="disabled")
        self._doi_trang_thai("Đang chạy... đừng tắt cửa sổ.", "#c60")
        self.nut_chay.configure(state="disabled")
        self.nut_dung.configure(state="normal")

        self.handler_log = gan_vao_logger(self.hang_doi_log, self.ten_logger)

        self.luong = LuongChay(ham_thu_thap=self.tao_ham_thu_thap(seeds))
        self.luong.start()

    def _dung(self) -> None:
        if self.luong is not None:
            self.luong.yeu_cau_dung()
            self._doi_trang_thai("Đang dừng... chờ hoàn tất lượt hiện tại.", "#c60")
            self.nut_dung.configure(state="disabled")

    def _hoan_tat(self, df: Optional[pd.DataFrame], loi: Optional[str]) -> None:
        """Dọn dẹp và hiển thị kết quả. LUÔN chạy ở luồng chính."""
        self.nut_chay.configure(state="normal")
        self.nut_dung.configure(state="disabled")

        if self.handler_log is not None:
            go_khoi_logger(self.handler_log, self.ten_logger)
            self.handler_log = None

        if loi is not None:
            self._doi_trang_thai("Có lỗi xảy ra.", "#c00")
            self.hop_log.them_dong(40, loi)
            messagebox.showerror("Lỗi", "Xem chi tiết ở ô tiến trình bên trên.")
            return

        if df is None or df.empty:
            self._doi_trang_thai("Không thu được kết quả nào.", "#c60")
            return

        self.bang_ket_qua.nap_du_lieu(df)

        try:
            self.duong_dan_file = self.xuat_file(df)
            self.nut_mo_file.configure(state="normal")
            self._doi_trang_thai(f"Xong. {len(df)} dòng đã lưu ra file.", "#0a7")
        except Exception as e:  # noqa: BLE001
            self._doi_trang_thai(f"Chạy xong nhưng không ghi được file: {e}", "#c00")

    # =========================================================================
    # TIỆN ÍCH
    # =========================================================================

    def _doc_hang_doi_log(self) -> None:
        """
        Nhịp tim của giao diện, chạy ở LUỒNG CHÍNH mỗi 120ms.

        Làm hai việc:
            1. Lấy log mới từ hàng đợi ra hiển thị
            2. Kiểm tra luồng nền chạy xong chưa để thu kết quả

        Việc 2 đặt ở đây thay vì để luồng nền tự gọi, vì luồng nền không được
        phép đụng vào tkinter (xem ghi chú trong worker.py).
        """
        try:
            while True:
                muc, dong = self.hang_doi_log.get_nowait()
                self.hop_log.them_dong(muc, dong)
        except queue.Empty:
            pass

        if self.luong is not None and not self.luong.is_alive():
            luong_xong, self.luong = self.luong, None
            self._hoan_tat(luong_xong.ket_qua, luong_xong.loi)

        self.after(CHU_KY_DOC_LOG_MS, self._doc_hang_doi_log)

    def _doi_trang_thai(self, chu: str, mau: str) -> None:
        self.nhan_trang_thai.configure(text=chu, foreground=mau)

    def _mo_file(self) -> None:
        if self.duong_dan_file and os.path.exists(self.duong_dan_file):
            self._mo_bang_windows(self.duong_dan_file)

    def _mo_thu_muc(self) -> None:
        thu_muc = os.path.abspath("output")
        os.makedirs(thu_muc, exist_ok=True)
        self._mo_bang_windows(thu_muc)

    @staticmethod
    def _mo_bang_windows(duong_dan: str) -> None:
        """Mở file hoặc thư mục bằng ứng dụng mặc định của hệ điều hành."""
        try:
            if sys.platform == "win32":
                os.startfile(duong_dan)  # noqa: S606 - chỉ mở file do chính app tạo
            else:
                subprocess.run(["xdg-open", duong_dan], check=False)
        except Exception as e:  # noqa: BLE001
            messagebox.showerror("Không mở được", str(e))
