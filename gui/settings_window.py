# -*- coding: utf-8 -*-
"""
Màn hình Cấu hình AI — nhập API key ngay trong ứng dụng.

VÌ SAO CẦN
    Trước đây muốn đổi key hay đổi model phải mở Notepad sửa file .env, mà file
    đó Windows còn ẩn đi theo mặc định. Với người không quen máy tính thì đây là
    rào cản thật, và mỗi lần hết hạn mức lại phải làm lại.

    Màn hình này ghi thẳng vào .env nhưng GIỮ NGUYÊN chú thích trong đó, nên ai
    thích sửa tay vẫn sửa được như cũ.

BẢO MẬT
    API key hiển thị dạng chấm tròn, có nút hiện/ẩn. Không bao giờ ghi key ra
    log hay in ra màn hình tiến trình.
"""

import threading
import tkinter as tk
import webbrowser
from tkinter import messagebox, ttk

from writer import config, env as env_util
from writer.providers import LoiGoiAI, tao_nha_cung_cap
from writer.settings import Settings, ThieuCauHinh


class CuaSoCauHinh(tk.Toplevel):
    """Hộp thoại chọn nhà cung cấp AI, nhập key và chọn model."""

    def __init__(self, cha, thu_muc_goc: str, khi_luu=None):
        super().__init__(cha)
        self.title("Cấu hình AI")
        self.geometry("620x560")
        self.resizable(False, False)

        self.thu_muc_goc = thu_muc_goc
        self.khi_luu = khi_luu
        self.dang_kiem_tra = False

        env_util.tao_env_tu_mau(thu_muc_goc)
        self.env = env_util.doc_env(thu_muc_goc)

        self._dung_giao_dien()
        self._nap_gia_tri()
        self.transient(cha)
        self.grab_set()

    # =========================================================================

    def _dung_giao_dien(self) -> None:
        khung = ttk.Frame(self, padding=14)
        khung.pack(fill="both", expand=True)

        ttk.Label(khung, text="Chọn AI viết bài",
                  font=("Segoe UI", 13, "bold")).pack(anchor="w")
        ttk.Label(khung, text="Cấu hình lưu vào file .env, không bao giờ đẩy lên GitHub.",
                  foreground="#555").pack(anchor="w", pady=(0, 12))

        # --- Chọn nhà cung cấp ---
        self.bien_ncc = tk.StringVar()
        khung_ncc = ttk.LabelFrame(khung, text="Nhà cung cấp", padding=10)
        khung_ncc.pack(fill="x", pady=(0, 12))
        for ma, tt in config.NHA_CUNG_CAP.items():
            hang = ttk.Frame(khung_ncc)
            hang.pack(fill="x", pady=2)
            ttk.Radiobutton(hang, text=tt["ten"], value=ma,
                            variable=self.bien_ncc,
                            command=self._doi_nha_cung_cap).pack(side="left")
            ttk.Label(hang, text=f"— {tt['ghi_chu']}",
                      foreground="#777", font=("Segoe UI", 8)).pack(side="left", padx=6)

        # --- API key ---
        khung_key = ttk.LabelFrame(khung, text="API key", padding=10)
        khung_key.pack(fill="x", pady=(0, 12))

        hang_key = ttk.Frame(khung_key)
        hang_key.pack(fill="x")
        self.bien_key = tk.StringVar()
        self.o_key = ttk.Entry(hang_key, textvariable=self.bien_key,
                               show="●", font=("Consolas", 10))
        self.o_key.pack(side="left", fill="x", expand=True)
        self.bien_hien = tk.BooleanVar(value=False)
        ttk.Checkbutton(hang_key, text="Hiện", variable=self.bien_hien,
                        command=self._bat_tat_hien_key).pack(side="left", padx=(6, 0))

        hang_lay = ttk.Frame(khung_key)
        hang_lay.pack(fill="x", pady=(6, 0))
        self.nhan_dang_key = ttk.Label(hang_lay, text="", foreground="#777",
                                       font=("Segoe UI", 8))
        self.nhan_dang_key.pack(side="left")
        self.nut_lay_key = ttk.Button(hang_lay, text="Lấy key ↗", width=11,
                                      command=self._mo_trang_lay_key)
        self.nut_lay_key.pack(side="right")

        # --- Model ---
        khung_model = ttk.LabelFrame(khung, text="Model", padding=10)
        khung_model.pack(fill="x", pady=(0, 12))
        hang_model = ttk.Frame(khung_model)
        hang_model.pack(fill="x")
        self.bien_model = tk.StringVar()
        self.o_model = ttk.Combobox(hang_model, textvariable=self.bien_model,
                                    font=("Consolas", 9))
        self.o_model.pack(side="left", fill="x", expand=True)
        ttk.Button(hang_model, text="Tải danh sách", width=14,
                   command=self._tai_danh_sach_model).pack(side="left", padx=(6, 0))
        ttk.Label(khung_model,
                  text="Gõ tay được. Bấm Tải danh sách để lấy model tài khoản bạn dùng được.",
                  foreground="#777", font=("Segoe UI", 8)).pack(anchor="w", pady=(4, 0))

        # --- Thông số ---
        khung_ts = ttk.LabelFrame(khung, text="Thông số", padding=10)
        khung_ts.pack(fill="x", pady=(0, 12))
        self.bien_max = tk.StringVar()
        self.bien_timeout = tk.StringVar()
        for cot, (nhan, bien, chu_thich) in enumerate([
            ("Độ dài tối đa (token):", self.bien_max, "3.000 từ ≈ 5.000 token"),
            ("Chờ tối đa (giây):", self.bien_timeout, "bài dài mất 120–250 giây"),
        ]):
            o = ttk.Frame(khung_ts)
            o.grid(row=cot, column=0, sticky="w", pady=2)
            ttk.Label(o, text=nhan, width=22).pack(side="left")
            ttk.Entry(o, textvariable=bien, width=10).pack(side="left")
            ttk.Label(o, text=f"  {chu_thich}", foreground="#777",
                      font=("Segoe UI", 8)).pack(side="left")

        # --- Trạng thái + nút ---
        self.nhan_trang_thai = ttk.Label(khung, text="", wraplength=580,
                                         justify="left")
        self.nhan_trang_thai.pack(anchor="w", pady=(0, 8))

        hang_nut = ttk.Frame(khung)
        hang_nut.pack(fill="x")
        self.nut_kiem_tra = ttk.Button(hang_nut, text="Kiểm tra kết nối",
                                       command=self._kiem_tra_ket_noi)
        self.nut_kiem_tra.pack(side="left")
        ttk.Button(hang_nut, text="Hủy", command=self.destroy).pack(side="right")
        self.nut_luu = ttk.Button(hang_nut, text="Lưu", command=self._luu)
        self.nut_luu.pack(side="right", padx=6)

    # =========================================================================

    def _nap_gia_tri(self) -> None:
        ncc = (self.env.get("NHA_CUNG_CAP") or config.NHA_CUNG_CAP_MAC_DINH).lower()
        if ncc not in config.NHA_CUNG_CAP:
            ncc = config.NHA_CUNG_CAP_MAC_DINH
        self.bien_ncc.set(ncc)
        self.bien_max.set(self.env.get("MAX_TOKENS") or str(config.MAX_TOKENS_MAC_DINH))
        self.bien_timeout.set(self.env.get("TIMEOUT") or str(config.TIMEOUT_MAC_DINH))
        self._doi_nha_cung_cap()

    def _doi_nha_cung_cap(self) -> None:
        """Đổi nhà cung cấp thì nạp lại key và model đã lưu của bên đó."""
        tt = config.NHA_CUNG_CAP[self.bien_ncc.get()]
        self.bien_key.set(self.env.get(tt["khoa_env"], ""))
        mac_dinh = {
            "gemini": config.GEMINI_MODEL_MAC_DINH,
            "openai": config.OPENAI_MODEL_MAC_DINH,
            "claude": config.CLAUDE_MODEL_MAC_DINH,
        }[self.bien_ncc.get()]
        self.bien_model.set(self.env.get(tt["model_env"]) or mac_dinh)
        self.o_model["values"] = []
        self.nhan_dang_key.configure(text=f"Key có dạng: {tt['dang_key']}")
        self._bao("", "#555")

    def _bat_tat_hien_key(self) -> None:
        self.o_key.configure(show="" if self.bien_hien.get() else "●")

    def _mo_trang_lay_key(self) -> None:
        webbrowser.open(config.NHA_CUNG_CAP[self.bien_ncc.get()]["lay_key"])

    # =========================================================================
    # KIỂM TRA / TẢI MODEL — chạy ở luồng nền để cửa sổ không đơ
    # =========================================================================

    def _settings_tam(self) -> Settings:
        """Dựng Settings từ những gì đang gõ trên màn hình, chưa cần lưu."""
        return Settings(
            nha_cung_cap=self.bien_ncc.get(),
            api_key=self.bien_key.get().strip(),
            model=self.bien_model.get().strip(),
            max_tokens=_so_nguyen(self.bien_max.get(), config.MAX_TOKENS_MAC_DINH),
            timeout=60,
            thu_muc_goc=self.thu_muc_goc,
        )

    def _chay_nen(self, viec, khi_xong) -> None:
        """
        Chạy việc gọi mạng ở luồng nền.

        Luồng nền KHÔNG được đụng vào giao diện, kể cả after() — nên nó chỉ cất
        kết quả vào biến, còn luồng chính định kỳ vào lấy.
        """
        if self.dang_kiem_tra:
            return
        self.dang_kiem_tra = True
        self.nut_kiem_tra.configure(state="disabled")
        ket_qua = {}

        def chay():
            try:
                ket_qua["ok"] = viec()
            except Exception as loi:  # noqa: BLE001
                ket_qua["loi"] = loi

        threading.Thread(target=chay, daemon=True).start()

        def doi():
            if "ok" not in ket_qua and "loi" not in ket_qua:
                self.after(120, doi)
                return
            self.dang_kiem_tra = False
            self.nut_kiem_tra.configure(state="normal")
            khi_xong(ket_qua.get("ok"), ket_qua.get("loi"))

        self.after(120, doi)

    def _kiem_tra_ket_noi(self) -> None:
        if not self.bien_key.get().strip():
            self._bao("Chưa nhập API key.", "#c00")
            return
        self._bao("Đang kiểm tra...", "#c60")
        st = self._settings_tam()

        def viec():
            return tao_nha_cung_cap(st).viet_bai("Trả lời đúng hai chữ: Xin chào")

        def xong(kq, loi):
            if loi is not None:
                self._bao(str(loi), "#c00")
            else:
                self._bao(f"✅ Kết nối tốt. Model trả lời: "
                          f"\"{kq.noi_dung.strip()[:60]}\"", "#0a7")

        self._chay_nen(viec, xong)

    def _tai_danh_sach_model(self) -> None:
        if not self.bien_key.get().strip():
            self._bao("Nhập API key trước đã.", "#c00")
            return
        self._bao("Đang tải danh sách model...", "#c60")
        st = self._settings_tam()

        def viec():
            ncc = tao_nha_cung_cap(st)
            if not hasattr(ncc, "liet_ke_model"):
                raise LoiGoiAI("Nhà cung cấp này chưa hỗ trợ tải danh sách model.\n"
                               "Bạn gõ tên model trực tiếp vào ô.")
            return ncc.liet_ke_model()

        def xong(ds, loi):
            if loi is not None:
                self._bao(str(loi), "#c00")
                return
            if not ds:
                self._bao("Không lấy được danh sách. Kiểm tra lại API key.", "#c00")
                return
            self.o_model["values"] = ds
            self._bao(f"Tìm thấy {len(ds)} model. Bấm mũi tên ở ô Model để chọn.", "#0a7")

        self._chay_nen(viec, xong)

    # =========================================================================

    def _luu(self) -> None:
        ncc = self.bien_ncc.get()
        tt = config.NHA_CUNG_CAP[ncc]
        key = self.bien_key.get().strip()

        if not key:
            if not messagebox.askyesno(
                    "Chưa có API key",
                    "Chưa nhập API key nên chưa viết bài được.\nVẫn lưu chứ?",
                    parent=self):
                return

        env_util.ghi_env(self.thu_muc_goc, {
            "NHA_CUNG_CAP": ncc,
            tt["khoa_env"]: key,
            tt["model_env"]: self.bien_model.get().strip(),
            "MAX_TOKENS": str(_so_nguyen(self.bien_max.get(), config.MAX_TOKENS_MAC_DINH)),
            "TIMEOUT": str(_so_nguyen(self.bien_timeout.get(), config.TIMEOUT_MAC_DINH)),
        })

        if self.khi_luu is not None:
            self.khi_luu()
        self.destroy()

    def _bao(self, chu: str, mau: str) -> None:
        self.nhan_trang_thai.configure(text=chu, foreground=mau)


def _so_nguyen(chuoi: str, mac_dinh: int) -> int:
    try:
        n = int(str(chuoi).strip())
        return n if n > 0 else mac_dinh
    except (TypeError, ValueError):
        return mac_dinh
