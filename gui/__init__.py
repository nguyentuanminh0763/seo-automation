# -*- coding: utf-8 -*-
"""
Giao diện đồ họa cho hai công cụ SEO. Dùng tkinter có sẵn trong Python,
KHÔNG cần cài thêm thư viện nào.

BẢN ĐỒ CÁC FILE:

    app.py         Cửa sổ chính, ghép hai tab lại.
    tab_base.py    Khung chung: ô nhập từ khóa, nút chạy/dừng, ô log, bảng kết quả.
                   Hai tab giống nhau tới 80% nên phần chung gom hết vào đây.
    tab_suggest.py Tab Google Suggest — chỉ khai báo phần tùy chọn riêng.
    tab_trends.py  Tab Google Trends — chỉ khai báo phần tùy chọn riêng.
    widgets.py     Thành phần dùng chung: ô log, bảng có lọc, ô nhập từ khóa.
    worker.py      Chạy công cụ ở luồng nền để cửa sổ không bị đơ.
    log_bridge.py  Đưa log từ luồng nền lên giao diện an toàn qua hàng đợi.

NGUYÊN TẮC QUAN TRỌNG:
    Package này KHÔNG chứa logic thu thập dữ liệu. Nó chỉ gọi lại đúng các hàm
    trong trends/ và suggest/. Sửa cách thu thập thì sửa ở hai package đó,
    giao diện tự động chạy theo.

Điểm chạy nằm ở file seo_gui.pyw bên ngoài package này.
"""

from .app import UngDung, chay

__all__ = ["UngDung", "chay"]
__version__ = "1.0.0"
