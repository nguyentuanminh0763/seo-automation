#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
 GIAO DIỆN SEO KEYWORD TOOLS — giaphongpc.vn
===============================================================================

 CÁCH CHẠY DỄ NHẤT: bấm đúp vào file  Chay_giao_dien.bat

 Hoặc chạy bằng lệnh:
     "C:\\Users\\PC\\AppData\\Local\\Programs\\Python\\Python312\\pythonw.exe" seo_gui.pyw

 Đuôi .pyw thay vì .py để Windows KHÔNG mở kèm cửa sổ đen dòng lệnh.

 File này chỉ khởi động ứng dụng. Toàn bộ giao diện nằm trong package gui/.
===============================================================================
"""

import os
import sys

# Đảm bảo Python tìm thấy các package trends/, suggest/, gui/ dù người dùng
# bấm đúp file từ bất kỳ đâu (thư mục làm việc lúc đó có thể không phải thư mục này).
THU_MUC_GOC = os.path.dirname(os.path.abspath(__file__))
if THU_MUC_GOC not in sys.path:
    sys.path.insert(0, THU_MUC_GOC)
os.chdir(THU_MUC_GOC)   # để file kết quả luôn ghi vào output/ cạnh script


def main() -> int:
    try:
        from gui import chay
    except ImportError as loi:
        _bao_loi_thieu_thu_vien(loi)
        return 1

    chay()
    return 0


def _bao_loi_thieu_thu_vien(loi: ImportError) -> None:
    """Thiếu thư viện thì hiện hộp thoại, không im lặng tắt ngóm."""
    thong_bao = (
        f"Không khởi động được ứng dụng.\n\n{loi}\n\n"
        "Nhiều khả năng thiếu thư viện. Mở PowerShell và chạy:\n\n"
        "python -m pip install -r requirements.txt"
    )
    try:
        import tkinter as tk
        from tkinter import messagebox
        goc = tk.Tk()
        goc.withdraw()
        messagebox.showerror("Lỗi khởi động", thong_bao)
    except Exception:  # noqa: BLE001 - không có cả tkinter thì đành in ra
        print(thong_bao)


if __name__ == "__main__":
    sys.exit(main())
