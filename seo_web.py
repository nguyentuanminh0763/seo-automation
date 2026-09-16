#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
 GIAO DIỆN WEB — SEO KEYWORD TOOLS (giaphongpc.vn)
===============================================================================

 CÁCH CHẠY DỄ NHẤT: bấm đúp vào file  Chay_giao_dien_web.bat

 Hoặc chạy bằng lệnh:
     "C:\\Users\\PC\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" seo_web.py

 Máy chủ chạy trong cửa sổ đen; trình duyệt tự mở ra. Đóng cửa sổ đen là tắt.

 KHÁC GÌ seo_gui.pyw?
     seo_gui.pyw  mở cửa sổ Windows (tkinter) — vẫn dùng bình thường
     seo_web.py   mở giao diện trong trình duyệt — cùng một công cụ bên dưới

 File này chỉ khởi động máy chủ. Toàn bộ API nằm trong package webapi/,
 giao diện nằm trong thư mục web/.
===============================================================================
"""

import argparse
import os
import sys

# Đảm bảo Python tìm thấy các package trends/, suggest/, webapi/ dù người dùng
# bấm đúp file từ bất kỳ đâu.
THU_MUC_GOC = os.path.dirname(os.path.abspath(__file__))
if THU_MUC_GOC not in sys.path:
    sys.path.insert(0, THU_MUC_GOC)
os.chdir(THU_MUC_GOC)   # để file kết quả luôn ghi vào output/ cạnh script


def doc_tham_so() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Giao diện web cho SEO Keyword Tools")
    p.add_argument("--cong", type=int, default=8765,
                   help="Cổng máy chủ (mặc định 8765). Bận thì tự nhảy cổng kế tiếp.")
    p.add_argument("--khong-mo-trinh-duyet", action="store_true",
                   help="Không tự mở trình duyệt khi khởi động")
    p.add_argument("--dev", action="store_true",
                   help="Chế độ lập trình giao diện: cho phép npm run dev "
                        "ở cổng 5173 gọi vào API này")
    return p.parse_args()


def main() -> int:
    tham_so = doc_tham_so()

    try:
        from webapi import chay
    except ImportError as loi:
        _bao_thieu_thu_vien(loi)
        return 1

    try:
        chay(THU_MUC_GOC,
             cong=tham_so.cong,
             dev=tham_so.dev,
             mo_trinh_duyet=not tham_so.khong_mo_trinh_duyet)
    except KeyboardInterrupt:
        print("\nĐã tắt máy chủ.")
    return 0


def _bao_thieu_thu_vien(loi: ImportError) -> None:
    """Thiếu thư viện thì in hướng dẫn rõ ràng, không để cửa sổ tắt ngóm."""
    print("=" * 62)
    print(" KHÔNG KHỞI ĐỘNG ĐƯỢC MÁY CHỦ WEB")
    print("=" * 62)
    print(f" Lý do: {loi}")
    print()
    print(" Nhiều khả năng thiếu thư viện. Mở PowerShell tại thư mục này")
    print(" và chạy đúng một lệnh sau:")
    print()
    print("     python -m pip install -r requirements.txt")
    print()
    print(" Nếu máy báo không tìm thấy python, dùng đường dẫn đầy đủ:")
    print(r'     "C:\Users\PC\AppData\Local\Programs\Python\Python312\python.exe"'
          " -m pip install -r requirements.txt")
    print("=" * 62)
    input(" Bấm Enter để đóng...")


if __name__ == "__main__":
    sys.exit(main())
