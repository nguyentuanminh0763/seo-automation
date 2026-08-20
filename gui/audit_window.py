# -*- coding: utf-8 -*-
"""
Cửa sổ hiển thị bảng kiểm tra SEO.

Thiết kế theo một nguyên tắc: người dùng không đọc bảng để biết mình giỏi,
mà để biết PHẢI SỬA GÌ. Nên các mục chưa đạt luôn nằm trên cùng, kèm gợi ý
cụ thể, và những câu có vấn đề được trích nguyên văn để copy đi sửa.
"""

import tkinter as tk
from tkinter import ttk

from writer.auditor import (CAN_NGUOI_KIEM, CHUA_DAT, DAT, KHONG_AP_DUNG,
                            BaoCaoKiemTra)

MAU = {
    CHUA_DAT: "#ffe0e0",
    DAT: "#e6f7e6",
    CAN_NGUOI_KIEM: "#fff6d9",
    KHONG_AP_DUNG: "#f0f0f0",
}


class CuaSoKiemTra(tk.Toplevel):
    """Cửa sổ riêng hiện bảng kiểm tra và các câu cần sửa."""

    def __init__(self, cha, bao_cao: BaoCaoKiemTra, noi_dung: str, tu_khoa: str):
        super().__init__(cha)
        self.title(f"Kiểm tra SEO — {tu_khoa}")
        self.geometry("980x680")
        self.minsize(760, 480)

        self.bao_cao = bao_cao
        self.noi_dung = noi_dung
        self.tu_khoa = tu_khoa

        self._dung_giao_dien()
        self.transient(cha)

    def _dung_giao_dien(self) -> None:
        khung = ttk.Frame(self, padding=10)
        khung.pack(fill="both", expand=True)

        # --- Dòng tóm tắt ---
        b = self.bao_cao
        mau_tom_tat = "#c00" if b.so_chua_dat else "#0a7"
        ttk.Label(khung, text=b.tom_tat(),
                  font=("Segoe UI", 12, "bold"), foreground=mau_tom_tat
                  ).pack(anchor="w")
        ttk.Label(
            khung,
            text=(f"{b.so_dat} đạt · {b.so_chua_dat} chưa đạt · "
                  f"{b.so_can_kiem} cần bạn tự đọc.\n"
                  "Các con số dưới đây do tool đếm, không phải AI tự khai. "
                  f"Phạm vi đếm: {b.pham_vi_dem}."),
            foreground="#555",
            justify="left",
        ).pack(anchor="w", pady=(0, 8))

        so_tay = ttk.Notebook(khung)
        so_tay.pack(fill="both", expand=True)

        so_tay.add(self._trang_bang(so_tay), text="  Bảng kiểm tra  ")

        # Lấy thẳng từ báo cáo chứ không đếm lại: bảng điểm chấm theo CỤM LÕI,
        # đếm lại bằng nguyên từ khóa sẽ ra danh sách ngắn hơn con số đã hiện.
        cau_nhoi = b.cau_nhoi
        so_bia = b.so_lieu_nghi_bia
        so_tay.add(
            self._trang_cau(so_tay, cau_nhoi, so_bia),
            text=f"  Câu cần sửa ({len(cau_nhoi) + len(so_bia)})  ",
        )

        ttk.Button(khung, text="Đóng", command=self.destroy).pack(anchor="e", pady=(8, 0))

    # ------------------------------------------------------------------

    def _trang_bang(self, cha) -> ttk.Frame:
        trang = ttk.Frame(cha, padding=8)

        cot = ("bieu_tuong", "ten", "chuan", "thuc_te", "goi_y")
        bang = ttk.Treeview(trang, columns=cot, show="headings", height=18)
        for ten_cot, tieu_de, rong in [
            ("bieu_tuong", "", 34),
            ("ten", "Tiêu chí", 210),
            ("chuan", "Chuẩn", 130),
            ("thuc_te", "Thực tế", 120),
            ("goi_y", "Cần làm gì", 420),
        ]:
            bang.heading(ten_cot, text=tieu_de)
            bang.column(ten_cot, width=rong, anchor="w",
                        stretch=(ten_cot == "goi_y"))

        for trang_thai, mau in MAU.items():
            bang.tag_configure(trang_thai, background=mau)

        # Chưa đạt lên đầu — người dùng mở bảng này để biết phải sửa gì.
        uu_tien = {CHUA_DAT: 0, CAN_NGUOI_KIEM: 1, DAT: 2, KHONG_AP_DUNG: 3}
        for muc in sorted(self.bao_cao.cac_muc,
                          key=lambda m: uu_tien.get(m.trang_thai, 9)):
            bang.insert("", "end", tags=(muc.trang_thai,), values=(
                muc.bieu_tuong, muc.ten, muc.chuan, muc.thuc_te, muc.goi_y,
            ))

        cuon = ttk.Scrollbar(trang, orient="vertical", command=bang.yview)
        bang.configure(yscrollcommand=cuon.set)
        bang.pack(side="left", fill="both", expand=True)
        cuon.pack(side="right", fill="y")
        return trang

    def _trang_cau(self, cha, cau_nhoi, so_bia) -> ttk.Frame:
        trang = ttk.Frame(cha, padding=8)

        o = tk.Text(trang, wrap="word", font=("Segoe UI", 10), padx=8, pady=8)
        cuon = ttk.Scrollbar(trang, orient="vertical", command=o.yview)
        o.configure(yscrollcommand=cuon.set)
        o.pack(side="left", fill="both", expand=True)
        cuon.pack(side="right", fill="y")

        o.tag_configure("tieu_de", font=("Segoe UI", 11, "bold"), spacing1=10, spacing3=4)
        o.tag_configure("giai_thich", foreground="#555", spacing3=8)
        o.tag_configure("cau", background="#fff6d9", spacing1=3, spacing3=3, lmargin1=14, lmargin2=14)
        o.tag_configure("khong_co", foreground="#0a7")

        if so_bia:
            o.insert("end", f"⚠ {len(so_bia)} chỗ có số liệu — kiểm tra xem có thật không\n", "tieu_de")
            o.insert("end",
                     "AI hay bịa phần trăm để câu văn nghe thuyết phục, kể cả khi prompt đã "
                     "cấm. Đối chiếu với số liệu thật của cửa hàng; không có số thật thì xóa "
                     "hoặc viết định tính.\n", "giai_thich")
            for c in so_bia:
                o.insert("end", f"  • {c}\n", "cau")

        if cau_nhoi:
            o.insert("end", f"\n⚠ {len(cau_nhoi)} câu lặp từ khóa từ 2 lần trở lên\n", "tieu_de")
            o.insert("end",
                     "Viết lại cho tự nhiên: giữ một lần, thay lần còn lại bằng "
                     "'lỗi này', 'hiện tượng trên'.\n", "giai_thich")
            for c in cau_nhoi:
                o.insert("end", f"  • {c}\n", "cau")

        if not so_bia and not cau_nhoi:
            o.insert("end", "✅ Không tìm thấy câu nhồi từ khóa hay số liệu đáng ngờ.\n\n", "khong_co")
            o.insert("end",
                     "Lưu ý: máy chỉ bắt được câu lặp từ khóa và câu chứa số. "
                     "Câu đọc lên thấy gượng thì vẫn cần bạn tự đọc lại.\n", "giai_thich")

        o.configure(state="disabled")
        return trang
