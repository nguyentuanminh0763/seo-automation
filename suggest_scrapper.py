#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
 SUGGEST SCRAPPER - Lấy keyword LÀM CONTENT từ Google Suggest
 Dành riêng cho: giaphongpc.vn
===============================================================================

 CÔNG CỤ NÀY KHÁC GÌ trends_scrapper.py?
     trends_scrapper.py   -> "Cái gì đang NÓNG LÊN tuần này?"  (5-10 từ, bắt trend)
     suggest_scrapper.py  -> "Người ta HAY HỎI GÌ?"            (hàng trăm từ, viết bài)

 ĐÂY CHỈ LÀ ĐIỂM CHẠY CHƯƠNG TRÌNH. Logic thật nằm trong package suggest/.
 Muốn sửa danh sách từ khóa -> mở file  suggest/config.py

 CÀI ĐẶT (chạy 1 lần):
     python -m pip install requests pandas openpyxl

 CÁCH CHẠY:
     python suggest_scrapper.py                    # đầy đủ, ~15-20 phút
     python suggest_scrapper.py --quick            # nhanh, bỏ quét bảng chữ cái
     python suggest_scrapper.py --seed-file s.txt  # nạp từ khóa gốc từ file .txt
     python suggest_scrapper.py --format csv       # xuất CSV thay vì Excel

 KẾT QUẢ: file Excel trong thư mục output/, đã chia sẵn sheet theo nhóm:
     Khắc phục lỗi | Khái niệm | Hướng dẫn | So sánh - Tư vấn | Thương mại
===============================================================================
"""

import argparse
import sys
import time
from datetime import datetime
from typing import List

from suggest import Settings, lay_log, thiet_lap_log, thu_thap, xuat_bao_cao
from suggest import config

log = lay_log()


def doc_tham_so() -> argparse.Namespace:
    """Khai báo tham số dòng lệnh. Mọi tham số đều ghi đè giá trị trong config.py."""
    parser = argparse.ArgumentParser(
        description="Lấy keyword làm content từ Google Suggest cho giaphongpc.vn"
    )
    parser.add_argument("--seed-file",
                        help="File .txt chứa từ khóa gốc, mỗi dòng một từ")
    parser.add_argument("--quick", action="store_true",
                        help="Chạy nhanh: bỏ qua phần quét bảng chữ cái a-z "
                             "(ít keyword hơn nhưng nhanh gấp ~3 lần)")
    parser.add_argument("--format", choices=["xlsx", "csv"], default="xlsx",
                        help="Định dạng file xuất ra (mặc định: xlsx)")
    return parser.parse_args()


def nap_seed(duong_dan_file: str) -> List[str]:
    """Nạp từ khóa gốc từ file, hoặc dùng danh sách mặc định trong suggest/config.py."""
    if not duong_dan_file:
        return config.SEED_KEYWORDS

    try:
        with open(duong_dan_file, "r", encoding="utf-8") as f:
            danh_sach = [dong.strip() for dong in f if dong.strip()]
        log.info("Đã nạp %d từ khóa gốc từ %s", len(danh_sach), duong_dan_file)
        return danh_sach
    except OSError as loi:
        log.error("Không đọc được file: %s -> dùng danh sách mặc định.", loi)
        return config.SEED_KEYWORDS


def in_thong_ke(df) -> None:
    """In bảng thống kê số keyword theo từng nhóm ý định."""
    print("\n--- SỐ KEYWORD THEO NHÓM ---")
    thong_ke = df.groupby("Nhóm ý định", sort=False).size()
    for nhom, so_luong in thong_ke.items():
        print(f"  {nhom:<22} {so_luong:>5} keyword")
    print()


def in_vi_du(df, so_dong: int = 15) -> None:
    """In vài keyword tiêu biểu để xem ngay chất lượng dữ liệu."""
    print(f"--- {so_dong} KEYWORD ƯU TIÊN LÀM TRƯỚC ---")
    cot = ["Keyword chính", "Nhóm ý định", "Loại bài đề xuất"]
    print(df.head(so_dong)[cot].to_string(index=False))
    print()


def main() -> int:
    thiet_lap_log()   # PHẢI gọi đầu tiên: ép UTF-8 để log tiếng Việt không vỡ

    tham_so = doc_tham_so()
    st = Settings.tu_cli(tham_so)
    danh_sach_seed = nap_seed(tham_so.seed_file)

    bat_dau = time.time()
    log.info("=" * 70)
    log.info("BẮT ĐẦU LẤY KEYWORD CONTENT - %s",
             datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    log.info("=" * 70)

    try:
        df = thu_thap(danh_sach_seed, st)
    except KeyboardInterrupt:
        log.warning("Người dùng đã dừng script (Ctrl+C).")
        return 1
    except Exception as loi:  # noqa: BLE001 - chốt chặn cuối cùng
        log.exception("Lỗi không lường trước: %s", loi)
        return 1

    log.info("=" * 70)

    if df.empty:
        log.warning("KHÔNG thu được keyword nào.")
        log.warning("Kiểm tra: máy có vào mạng được không, hoặc IP có đang bị chặn không.")
        return 0

    duong_dan = xuat_bao_cao(df, st)

    log.info("HOÀN TẤT sau %.1f phút.", (time.time() - bat_dau) / 60)
    log.info("Tổng số keyword thu được: %d", len(df))
    log.info("File báo cáo: %s", duong_dan)
    log.info("=" * 70)

    in_thong_ke(df)
    in_vi_du(df)
    return 0


if __name__ == "__main__":
    sys.exit(main())
