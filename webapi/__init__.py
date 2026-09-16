# -*- coding: utf-8 -*-
"""
Package máy chủ web nội bộ — cầu nối giữa giao diện React và ba công cụ Python.

KHÁC GÌ PACKAGE gui/?
    gui/     giao diện tkinter, chạy thẳng trên máy, cửa sổ Windows
    webapi/  giao diện web, mở bằng trình duyệt — cùng một logic bên dưới

NGUYÊN TẮC BẮT BUỘC — GIỐNG HỆT gui/:
    Package này KHÔNG chứa logic thu thập. Nó chỉ gọi lại các hàm có sẵn trong
    trends/, suggest/, writer/. Sửa cách thu thập thì sửa ở đó, không sửa ở đây.

    Máy chủ chỉ nghe ở 127.0.0.1 (máy của bạn). Không ai ngoài internet vào được.

BẢN ĐỒ CÁC FILE:

    config.py       Hằng số: cổng, thư mục web, giới hạn. File bạn sửa nếu cần.
    log_bridge.py   Đưa log của công cụ vào hàng đợi (giống gui/log_bridge.py).
    jobs.py         Quản lý việc chạy nền: tạo, theo dõi, dừng, dọn dẹp.
    runners.py      Ba hàm chạy thật: Trends, Suggest, Viết bài.
    serializers.py  Đổi DataFrame / báo cáo SEO sang JSON cho trình duyệt đọc.
    routes.py       Khai báo đường dẫn API — thêm tính năng thì sửa file này.
    server.py       Máy chủ HTTP, phục vụ file giao diện đã build.

Điểm chạy nằm ở file seo_web.py bên ngoài package này.
"""

__version__ = "1.0.0"
