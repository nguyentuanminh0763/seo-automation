#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
 TRENDS SCRAPPER - Dò tìm từ khóa ĐỘT BIẾN (Breakout) trên Google Trends
 Dành riêng cho: giaphongpc.vn (PC lắp ráp, Laptop, Linh kiện, Màn hình, Gaming Gear)
===============================================================================

 ĐÂY CHỈ LÀ ĐIỂM CHẠY CHƯƠNG TRÌNH. Logic thật nằm trong package trends/.
 Muốn sửa danh sách từ khóa -> mở file  trends/config.py

 CÀI ĐẶT (chạy 1 lần):
     python -m pip install pytrends pandas openpyxl

 CÁCH CHẠY:
     python trends_scrapper.py                          # cấu hình mặc định
     python trends_scrapper.py --timeframe "today 3-m"  # đổi khung thời gian
     python trends_scrapper.py --seed-file seeds.txt    # nạp seed từ file .txt
     python trends_scrapper.py --include-rising         # lấy thêm từ khóa tăng mạnh
     python trends_scrapper.py --format csv             # xuất CSV thay vì Excel

 LƯU Ý: PyTrends là API KHÔNG CHÍNH THỨC. Nếu gặp lỗi 429 nghĩa là IP đang bị chặn,
 hãy đợi vài giờ hoặc khai báo proxy trong trends/config.py.
===============================================================================
"""

import argparse
import sys
import time
from datetime import datetime
from typing import List

from trends import Settings, lay_log, quet_breakout, thiet_lap_log, xuat_bao_cao
from trends import config

log = lay_log()


def doc_tham_so() -> argparse.Namespace:
    """Khai báo tham số dòng lệnh. Mọi tham số đều ghi đè giá trị trong config.py."""
    parser = argparse.ArgumentParser(
        description="Dò từ khóa Breakout trên Google Trends cho giaphongpc.vn"
    )
    parser.add_argument("--seed-file",
                        help="File .txt chứa seed keywords, mỗi dòng một từ khóa")
    parser.add_argument("--timeframe", default=config.TIMEFRAME,
                        help="Khung thời gian: 'today 1-m' (mặc định), 'today 3-m', 'now 7-d'")
    parser.add_argument("--geo", default=config.GEO,
                        help="Mã khu vực: VN (mặc định), VN-SG, VN-HN")
    parser.add_argument("--include-rising", action="store_true",
                        help=f"Lấy thêm từ khóa Rising >= {config.RISING_THRESHOLD}%%, "
                             "không chỉ riêng Breakout")
    parser.add_argument("--format", choices=["xlsx", "csv"], default="xlsx",
                        help="Định dạng file xuất ra (mặc định: xlsx)")
    return parser.parse_args()


def nap_seed(duong_dan_file: str) -> List[str]:
    """
    Nạp danh sách từ khóa hạt giống.

    Ưu tiên file do người dùng chỉ định; nếu không có hoặc lỗi thì dùng
    danh sách mặc định trong trends/config.py.
    """
    if not duong_dan_file:
        return config.SEED_KEYWORDS

    try:
        with open(duong_dan_file, "r", encoding="utf-8") as f:
            danh_sach = [dong.strip() for dong in f if dong.strip()]
        log.info("Đã nạp %d từ khóa từ %s", len(danh_sach), duong_dan_file)
        return danh_sach
    except OSError as loi:
        log.error("Không đọc được file seed: %s -> dùng danh sách mặc định.", loi)
        return config.SEED_KEYWORDS


def in_ket_qua_rong() -> None:
    """Hướng dẫn xử lý khi không tìm được từ khóa nào."""
    log.warning("KHÔNG tìm thấy từ khóa Breakout nào.")
    log.warning("Gợi ý xử lý:")
    log.warning("  1. Nới khung thời gian:  --timeframe \"today 3-m\"")
    log.warning("  2. Hạ ngưỡng lọc:        --include-rising")
    log.warning("  3. Nếu log có lỗi 429 -> IP đang bị chặn, đợi vài giờ hoặc dùng proxy.")


def in_top_10(df) -> None:
    """In nhanh 10 từ khóa đột biến đáng chú ý nhất ra màn hình."""
    cot_hien_thi = ["Seed Keyword", "Breakout Keyword", "Query Type", "Growth (%)"]
    print("\n--- TOP 10 TỪ KHÓA ĐỘT BIẾN ---")
    print(df.head(10)[cot_hien_thi].to_string(index=False))
    print()


def main() -> int:
    thiet_lap_log()   # PHẢI gọi đầu tiên: ép UTF-8 để log tiếng Việt không vỡ

    tham_so = doc_tham_so()
    st = Settings.tu_cli(tham_so)
    danh_sach_seed = nap_seed(tham_so.seed_file)

    bat_dau = time.time()
    log.info("=" * 70)
    log.info("BẮT ĐẦU QUÉT GOOGLE TRENDS - %s",
             datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    log.info("=" * 70)

    try:
        df = quet_breakout(danh_sach_seed, st)
    except KeyboardInterrupt:
        log.warning("Người dùng đã dừng script (Ctrl+C).")
        return 1
    except Exception as loi:  # noqa: BLE001 - chốt chặn cuối cùng, không để script sập
        log.exception("Lỗi không lường trước: %s", loi)
        return 1

    log.info("=" * 70)

    if df.empty:
        in_ket_qua_rong()
        return 0

    duong_dan = xuat_bao_cao(df, st)
    so_breakout = int((df["Query Type"] == "Breakout").sum())

    log.info("HOÀN TẤT sau %.1f giây.", time.time() - bat_dau)
    log.info("Tổng số dòng: %d  |  Breakout thực sự: %d", len(df), so_breakout)
    log.info("File báo cáo: %s", duong_dan)
    log.info("=" * 70)

    in_top_10(df)
    return 0


if __name__ == "__main__":
    sys.exit(main())
