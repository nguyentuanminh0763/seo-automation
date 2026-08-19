# -*- coding: utf-8 -*-
"""
Package dò tìm từ khóa đột biến (Breakout) trên Google Trends cho giaphongpc.vn.

BẢN ĐỒ CÁC FILE - cần sửa gì thì mở đúng file đó:

    config.py    Hằng số cấu hình. ĐÂY LÀ FILE BẠN SỬA HÀNG NGÀY (danh sách từ khóa,
                 khu vực, khung thời gian, độ trễ chống chặn, proxy...).
    settings.py  Gói cấu hình thành đối tượng Settings, gộp với tham số dòng lệnh.
    logger.py    Thiết lập log + ép UTF-8 cho console Windows.
    client.py    Tạo kết nối Google Trends, xoay proxy, đổi User-Agent, nghỉ ngẫu nhiên.
    fetcher.py   Gọi API kèm retry - toàn bộ logic chống chặn IP nằm ở đây.
    filters.py   Lọc ra từ khóa Breakout. Đây là phần "não" của công cụ.
    scanner.py   Điều phối: chia nhóm 5 từ -> gọi API -> lọc -> gom DataFrame.
    exporter.py  Xuất báo cáo Excel/CSV.

Điểm chạy chương trình nằm ở file trends_scrapper.py bên ngoài package này.
"""

from .exporter import xuat_bao_cao
from .logger import lay_log, thiet_lap_log
from .scanner import quet_breakout
from .settings import Settings

__all__ = ["Settings", "quet_breakout", "xuat_bao_cao", "thiet_lap_log", "lay_log"]
__version__ = "2.0.0"
