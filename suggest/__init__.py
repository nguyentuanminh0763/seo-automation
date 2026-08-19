# -*- coding: utf-8 -*-
"""
Package thu thập keyword làm CONTENT từ Google Suggest, cho giaphongpc.vn.

Khác gì package trends/?
    trends/   trả lời "cái gì đang NÓNG LÊN tuần này?"  -> bắt trend, canh nhập hàng
    suggest/  trả lời "người ta HAY HỎI GÌ?"            -> lên kế hoạch viết bài

BẢN ĐỒ CÁC FILE - cần sửa gì thì mở đúng file đó:

    config.py      Hằng số cấu hình. ĐÂY LÀ FILE BẠN SỬA (từ khóa gốc, từ mồi,
                   luật phân loại, bộ lọc rác).
    settings.py    Gói cấu hình thành đối tượng Settings, gộp với tham số dòng lệnh.
    logger.py      Thiết lập log + ép UTF-8 cho console Windows.
    expander.py    Sinh biến thể truy vấn từ một từ gốc (công thức của dân SEO).
    client.py      Gọi Google Suggest kèm retry, xoay proxy, đổi User-Agent.
    classifier.py  Phân loại ý định tìm kiếm + đề xuất loại bài. Phần "não".
    collector.py   Điều phối: sinh biến thể -> hỏi -> lọc -> phân loại -> gom bảng.
    exporter.py    Xuất Excel nhiều sheet chia sẵn theo nhóm ý định.

Điểm chạy chương trình nằm ở file suggest_scrapper.py bên ngoài package này.
"""

from .collector import thu_thap
from .exporter import xuat_bao_cao
from .logger import lay_log, thiet_lap_log
from .settings import Settings

__all__ = ["Settings", "thu_thap", "xuat_bao_cao", "thiet_lap_log", "lay_log"]
__version__ = "1.0.0"
