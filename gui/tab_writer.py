# -*- coding: utf-8 -*-
"""
Tab "Viết bài" — nhập từ khóa, chọn prompt, gọi AI, copy sang WordPress.

Không kế thừa TabCoSo như hai tab kia vì hình dạng khác hẳn: không có danh
sách từ khóa gốc, không có bảng kết quả, mà là một ô soạn thảo lớn.
"""

import os
import queue
import tkinter as tk
from tkinter import messagebox, ttk
from typing import List, Optional

from writer import (BaiViet, LoiGoiAI, Prompt, Settings, ThieuCauHinh,
                    liet_ke_prompt, luu_bai, viet_bai)
from writer import clipboard as bang_nho_tam
from writer import env as env_util
from writer.prompts import huong_dan_khi_rong

from .log_bridge import gan_vao_logger, go_khoi_logger
from .tab_base import CHU_KY_DOC_LOG_MS
from .widgets import HopLog
from .worker import LuongChay


class TabWriter(ttk.Frame):
    """Tab viết bài bằng AI."""

    def __init__(self, cha, thu_muc_goc: str):
        super().__init__(cha, padding=10)

        self.thu_muc_goc = thu_muc_goc
        self.hang_doi_log: "queue.Queue" = queue.Queue()
        self.luong: Optional[LuongChay] = None
        self.handler_log = None
        self.bai_hien_tai: Optional[BaiViet] = None
        self.duong_dan_file: Optional[str] = None
        self.danh_sach_prompt: List[Prompt] = []

        self._dung_giao_dien()
        self._nap_prompt()
        self._kiem_tra_cau_hinh()
        self._doc_hang_doi_log()

    # =========================================================================
    # DỰNG GIAO DIỆN
    # =========================================================================

    def _dung_giao_dien(self) -> None:
        ttk.Label(self, text="Viết bài bằng AI",
                  font=("Segoe UI", 13, "bold")).grid(row=0, column=0, columnspan=2, sticky="w")
        ttk.Label(self, text="Dán từ khóa, chọn prompt, bấm Viết. "
                             "Xong thì copy dán thẳng vào WordPress.",
                  foreground="#555").grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 10))

        # --- CỘT TRÁI: nhập liệu ---
        trai = ttk.Frame(self)
        trai.grid(row=2, column=0, sticky="nsew", padx=(0, 12))

        ttk.Label(trai, text="Từ khóa:", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.bien_keyword = tk.StringVar()
        o_keyword = ttk.Entry(trai, textvariable=self.bien_keyword, width=38,
                              font=("Segoe UI", 10))
        o_keyword.pack(fill="x", pady=(4, 10))
        o_keyword.bind("<Return>", lambda _e: self._bat_dau())

        ttk.Label(trai, text="Prompt:", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        khung_prompt = ttk.Frame(trai)
        khung_prompt.pack(fill="x", pady=(4, 2))
        self.bien_prompt = tk.StringVar()
        self.o_chon_prompt = ttk.Combobox(khung_prompt, textvariable=self.bien_prompt,
                                          state="readonly", width=26)
        self.o_chon_prompt.pack(side="left", fill="x", expand=True)
        ttk.Button(khung_prompt, text="Nạp lại", width=8,
                   command=self._nap_prompt).pack(side="left", padx=(4, 0))

        ttk.Button(trai, text="Mở thư mục prompt để sửa",
                   command=self._mo_thu_muc_prompt).pack(fill="x", pady=(0, 10))

        ttk.Label(trai, text="Ghi chú thêm cho riêng bài này:",
                  font=("Segoe UI", 9, "bold")).pack(anchor="w")
        ttk.Label(trai, text="Giá hiện tại, khuyến mãi, model cụ thể...",
                  foreground="#777", font=("Segoe UI", 8)).pack(anchor="w")
        self.o_ghi_chu = tk.Text(trai, height=6, width=36, wrap="word",
                                 font=("Segoe UI", 9))
        self.o_ghi_chu.pack(fill="both", expand=True, pady=(4, 10))

        self.nut_viet = ttk.Button(trai, text="✎  Viết bài", command=self._bat_dau)
        self.nut_viet.pack(fill="x", pady=2)

        hang_ai = ttk.Frame(trai)
        hang_ai.pack(fill="x", pady=(6, 0))
        self.nhan_ai = ttk.Label(hang_ai, text="", foreground="#0a7",
                                 font=("Segoe UI", 8), wraplength=190, justify="left")
        self.nhan_ai.pack(side="left", fill="x", expand=True)
        ttk.Button(hang_ai, text="⚙", width=3,
                   command=self._mo_cau_hinh).pack(side="right")
        ttk.Button(trai, text="Cấu hình AI · đổi key, đổi model",
                   command=self._mo_cau_hinh).pack(fill="x", pady=(4, 0))

        # --- CỘT PHẢI: kết quả ---
        phai = ttk.Frame(self)
        phai.grid(row=2, column=1, sticky="nsew")

        ttk.Label(phai, text="Bài viết:", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        khung_bai = ttk.Frame(phai)
        khung_bai.pack(fill="both", expand=True, pady=(4, 6))
        self.o_bai = tk.Text(khung_bai, wrap="word", font=("Segoe UI", 10),
                             undo=True, height=18)
        cuon = ttk.Scrollbar(khung_bai, orient="vertical", command=self.o_bai.yview)
        self.o_bai.configure(yscrollcommand=cuon.set)
        self.o_bai.pack(side="left", fill="both", expand=True)
        cuon.pack(side="right", fill="y")

        # Tô đỏ những chỗ AI chừa lại cho người dùng điền số liệu thật
        self.o_bai.tag_configure("can_bo_sung", background="#ffe9a8")

        # --- Nút thao tác ---
        hang_nut = ttk.Frame(phai)
        hang_nut.pack(fill="x", pady=(0, 6))
        self.nut_copy = ttk.Button(hang_nut, text="📋  Copy để dán WordPress",
                                   command=self._copy_dinh_dang, state="disabled")
        self.nut_copy.pack(side="left", padx=(0, 4))
        self.nut_mo_trinh_duyet = ttk.Button(hang_nut, text="🌐  Mở bằng trình duyệt",
                                             command=self._mo_trinh_duyet, state="disabled")
        self.nut_mo_trinh_duyet.pack(side="left", padx=4)
        self.nut_copy_html = ttk.Button(hang_nut, text="Copy mã HTML",
                                        command=self._copy_ma_html, state="disabled")
        self.nut_copy_html.pack(side="left", padx=4)
        self.nut_kiem_tra = ttk.Button(hang_nut, text="🔍  Kiểm tra SEO",
                                       command=self._mo_bang_kiem_tra, state="disabled")
        self.nut_kiem_tra.pack(side="left", padx=4)

        ttk.Label(phai, text="Tiến trình:", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.hop_log = HopLog(phai)
        self.hop_log.pack(fill="x", pady=(4, 6))

        self.nhan_trang_thai = ttk.Label(phai, text="Sẵn sàng.", foreground="#0a7")
        self.nhan_trang_thai.pack(anchor="w")

        self.columnconfigure(1, weight=3)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

    # =========================================================================
    # NẠP DỮ LIỆU
    # =========================================================================

    def _nap_prompt(self) -> None:
        """Đọc lại thư mục prompts/. Gọi khi mở app và khi bấm 'Nạp lại'."""
        self.danh_sach_prompt = liet_ke_prompt(self.thu_muc_goc)
        ten_cac_prompt = [p.ten for p in self.danh_sach_prompt]

        self.o_chon_prompt["values"] = ten_cac_prompt
        if ten_cac_prompt:
            if self.bien_prompt.get() not in ten_cac_prompt:
                self.bien_prompt.set(ten_cac_prompt[0])
        else:
            self.bien_prompt.set("")
            self._doi_trang_thai("Chưa có file prompt nào.", "#c60")

    def _kiem_tra_cau_hinh(self) -> None:
        """Kiểm tra .env ngay khi mở tab, báo sớm thay vì để lỗi lúc bấm Viết."""
        if env_util.thieu_file_env(self.thu_muc_goc):
            self.nhan_ai.configure(text="⚠ Chưa có file .env — bấm Viết để xem hướng dẫn",
                                   foreground="#c60")
            return
        try:
            st = Settings.tu_env(self.thu_muc_goc)
            self.nhan_ai.configure(text=f"Đang dùng: {st.mo_ta()}", foreground="#0a7")
        except ThieuCauHinh as loi:
            self.nhan_ai.configure(text=f"⚠ {str(loi).splitlines()[0]}", foreground="#c60")

    def _prompt_dang_chon(self) -> Optional[Prompt]:
        ten = self.bien_prompt.get()
        for p in self.danh_sach_prompt:
            if p.ten == ten:
                return p
        return None

    # =========================================================================
    # VIẾT BÀI
    # =========================================================================

    def _bat_dau(self) -> None:
        keyword = self.bien_keyword.get().strip()
        if not keyword:
            messagebox.showwarning("Thiếu từ khóa", "Hãy nhập hoặc dán từ khóa cần viết.")
            return

        try:
            st = Settings.tu_env(self.thu_muc_goc)
        except ThieuCauHinh as loi:
            # Thiếu key thì mở thẳng màn hình cấu hình thay vì chỉ báo lỗi —
            # người dùng đang muốn viết bài, đừng bắt họ tự đi tìm chỗ sửa.
            if messagebox.askyesno("Chưa có API key",
                                   f"{loi}\n\nMở màn hình Cấu hình AI ngay bây giờ?"):
                self._mo_cau_hinh()
            return

        prompt = self._prompt_dang_chon()
        if prompt is None:
            messagebox.showerror("Chưa có prompt", huong_dan_khi_rong(self.thu_muc_goc))
            return

        ghi_chu = self.o_ghi_chu.get("1.0", "end").strip()

        self.hop_log.xoa_sach()
        self._xoa_ket_qua()
        self._doi_trang_thai("Đang viết... thường mất 20–60 giây.", "#c60")
        self.nut_viet.configure(state="disabled")
        self.handler_log = gan_vao_logger(self.hang_doi_log, "writer")

        self.luong = LuongChay(
            ham_thu_thap=lambda _nen_dung: viet_bai(keyword, prompt, st, ghi_chu)
        )
        self.luong.start()

    def _hoan_tat(self, bai, loi: Optional[str]) -> None:
        """Chạy ở luồng chính, do vòng lặp _doc_hang_doi_log gọi."""
        self.nut_viet.configure(state="normal")

        if self.handler_log is not None:
            go_khoi_logger(self.handler_log, "writer")
            self.handler_log = None

        if loi is not None:
            self._doi_trang_thai("Có lỗi xảy ra.", "#c00")
            self.hop_log.them_dong(40, loi)
            messagebox.showerror("Không viết được bài", loi)
            return

        if bai is None:
            self._doi_trang_thai("Không nhận được nội dung.", "#c60")
            return

        self.bai_hien_tai = bai
        self._hien_bai(bai)

        try:
            self.duong_dan_file = luu_bai(bai, self.thu_muc_goc)
        except OSError as e:
            self.duong_dan_file = None
            self.hop_log.them_dong(30, f"Không lưu được file: {e}")

        for nut in (self.nut_copy, self.nut_mo_trinh_duyet,
                    self.nut_copy_html, self.nut_kiem_tra):
            nut.configure(state="normal")

        # Chạy kiểm tra ngay để người dùng thấy vấn đề trước khi kịp copy đi đăng.
        bao_cao = self._chay_kiem_tra()

        phan_them = ""
        if bai.so_cho_can_bo_sung:
            phan_them += f" · {bai.so_cho_can_bo_sung} chỗ cần điền số liệu"
        if bao_cao is not None:
            phan_them += f" · {bao_cao.tom_tat()}"

        co_van_de = bai.so_cho_can_bo_sung or (bao_cao and bao_cao.so_chua_dat)
        self._doi_trang_thai(
            f"Xong. {bai.so_tu} từ · {bai.mo_ta_chi_phi}{phan_them}",
            "#c60" if co_van_de else "#0a7",
        )

    def _hien_bai(self, bai: BaiViet) -> None:
        """Đổ bài viết vào ô soạn thảo và tô vàng chỗ cần bổ sung."""
        self.o_bai.delete("1.0", "end")
        self.o_bai.insert("1.0", bai.markdown)

        # Tô vàng mọi dòng chứa [CẦN BỔ SUNG: ...]
        from writer.config import DAU_HIEU_CAN_BO_SUNG
        vi_tri = "1.0"
        while True:
            vi_tri = self.o_bai.search(DAU_HIEU_CAN_BO_SUNG, vi_tri, stopindex="end")
            if not vi_tri:
                break
            cuoi = self.o_bai.search("]", vi_tri, stopindex="end")
            cuoi = f"{cuoi}+1c" if cuoi else f"{vi_tri} lineend"
            self.o_bai.tag_add("can_bo_sung", vi_tri, cuoi)
            vi_tri = cuoi

    def _xoa_ket_qua(self) -> None:
        self.bai_hien_tai = None
        self.duong_dan_file = None
        self.o_bai.delete("1.0", "end")
        for nut in (self.nut_copy, self.nut_mo_trinh_duyet,
                    self.nut_copy_html, self.nut_kiem_tra):
            nut.configure(state="disabled")

    # =========================================================================
    # KIỂM TRA SEO
    # =========================================================================

    def _chay_kiem_tra(self):
        """
        Đếm lại trên nội dung ĐANG hiển thị, không phải bản AI trả về ban đầu —
        người dùng sửa tay xong bấm kiểm tra lại phải ra số mới.
        """
        from writer import auditor

        noi_dung = self._lay_ban_dang_sua()
        if not noi_dung or self.bai_hien_tai is None:
            return None
        try:
            return auditor.kiem_tra(noi_dung, self.bai_hien_tai.keyword)
        except Exception as loi:  # noqa: BLE001 - kiểm tra hỏng không được chặn việc dùng bài
            self.hop_log.them_dong(30, f"Không chạy được kiểm tra SEO: {loi}")
            return None

    def _mo_bang_kiem_tra(self) -> None:
        from .audit_window import CuaSoKiemTra

        bao_cao = self._chay_kiem_tra()
        if bao_cao is None:
            return
        CuaSoKiemTra(self, bao_cao, self._lay_ban_dang_sua(),
                     self.bai_hien_tai.keyword)

    # =========================================================================
    # COPY / MỞ
    # =========================================================================

    def _lay_ban_dang_sua(self) -> str:
        """Lấy nội dung hiện trong ô soạn thảo — người dùng có thể đã sửa tay."""
        return self.o_bai.get("1.0", "end").strip()

    def _copy_dinh_dang(self) -> None:
        """Copy kèm định dạng, dán thẳng vào WordPress ăn đúng tiêu đề."""
        from writer import formatter

        markdown = self._lay_ban_dang_sua()
        if not markdown:
            return
        html = formatter.sang_html(markdown)

        try:
            bang_nho_tam.chep_kem_dinh_dang(html, markdown)
            self._doi_trang_thai(
                "Đã copy. Sang WordPress bấm Ctrl+V. Nếu mất định dạng, "
                "dùng nút 'Mở bằng trình duyệt'.", "#0a7")
        except bang_nho_tam.LoiClipboard as loi:
            bang_nho_tam.chep_chu_thuong(self, markdown)
            messagebox.showwarning(
                "Chỉ copy được chữ thường",
                f"{loi}\n\nĐã copy bản chữ thường. Muốn giữ định dạng, "
                f"hãy dùng nút 'Mở bằng trình duyệt' rồi Ctrl+A, Ctrl+C.")

    def _copy_ma_html(self) -> None:
        """Copy mã HTML thô, dành cho chế độ Trình chỉnh sửa mã của WordPress."""
        from writer import formatter

        markdown = self._lay_ban_dang_sua()
        if not markdown:
            return
        bang_nho_tam.chep_chu_thuong(self, formatter.sang_html(markdown))
        self._doi_trang_thai(
            "Đã copy mã HTML. Trong WordPress chọn Trình chỉnh sửa mã rồi dán.", "#0a7")

    def _mo_trinh_duyet(self) -> None:
        """
        Đường lui chắc chắn nhất: mở file HTML bằng trình duyệt.
        Ctrl+A rồi Ctrl+C ở đó sẽ cho kết quả y hệt copy từ ChatGPT.
        """
        from writer import formatter, generator

        markdown = self._lay_ban_dang_sua()
        if not markdown or self.bai_hien_tai is None:
            return

        # Lưu lại bản người dùng đang sửa, không phải bản AI trả về ban đầu
        self.bai_hien_tai.markdown = markdown
        self.bai_hien_tai.html = formatter.sang_html(markdown)

        try:
            self.duong_dan_file = generator.luu_bai(self.bai_hien_tai, self.thu_muc_goc)
        except OSError as e:
            messagebox.showerror("Không lưu được file", str(e))
            return

        try:
            os.startfile(self.duong_dan_file)  # noqa: S606 - file do chính app tạo
            self._doi_trang_thai(
                "Đã mở trình duyệt. Bấm Ctrl+A rồi Ctrl+C, sang WordPress dán.", "#0a7")
        except OSError as e:
            messagebox.showerror("Không mở được", str(e))

    def _mo_cau_hinh(self) -> None:
        """Mở màn hình nhập API key, chọn nhà cung cấp và model."""
        from .settings_window import CuaSoCauHinh

        CuaSoCauHinh(self, self.thu_muc_goc, khi_luu=self._kiem_tra_cau_hinh)

    def _mo_thu_muc_prompt(self) -> None:
        from writer.config import THU_MUC_PROMPT

        thu_muc = os.path.join(self.thu_muc_goc, THU_MUC_PROMPT)
        os.makedirs(thu_muc, exist_ok=True)
        try:
            os.startfile(thu_muc)  # noqa: S606
        except OSError as e:
            messagebox.showerror("Không mở được", str(e))

    # =========================================================================
    # TIỆN ÍCH
    # =========================================================================

    def _doc_hang_doi_log(self) -> None:
        """Nhịp tim: đọc log và kiểm tra luồng nền xong chưa. Luôn ở luồng chính."""
        try:
            while True:
                muc, dong = self.hang_doi_log.get_nowait()
                self.hop_log.them_dong(muc, dong)
        except queue.Empty:
            pass

        if self.luong is not None and not self.luong.is_alive():
            luong_xong, self.luong = self.luong, None
            # Dùng thông điệp NGUYÊN VĂN của lỗi, không phải traceback cắt cụt.
            thong_bao = str(luong_xong.loi_goc) if luong_xong.loi_goc else None
            self._hoan_tat(luong_xong.ket_qua, thong_bao)

        self.after(CHU_KY_DOC_LOG_MS, self._doc_hang_doi_log)

    def _doi_trang_thai(self, chu: str, mau: str) -> None:
        self.nhan_trang_thai.configure(text=chu, foreground=mau)
