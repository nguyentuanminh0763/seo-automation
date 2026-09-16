# -*- coding: utf-8 -*-
"""
HẰNG SỐ CỦA MÁY CHỦ WEB — file duy nhất bạn cần sửa trong package này.

Chỉ chứa hằng số, không có logic. Sửa thoải mái không sợ vỡ code.
"""

# =============================================================================
# 1. MÁY CHỦ
# =============================================================================
# Chỉ nghe ở máy của bạn. ĐỪNG đổi thành "0.0.0.0" — làm vậy là mở cửa cho cả
# mạng LAN gọi vào, mà API này có quyền đọc/ghi file .env chứa API key.
DIA_CHI = "127.0.0.1"
CONG = 8765

# Tên miền được phép gọi API. Trình duyệt gửi kèm trong header Host.
# Danh sách này chặn kiểu tấn công DNS rebinding (một trang web bên ngoài trỏ
# tên miền của họ về 127.0.0.1 rồi gọi API của bạn).
HOST_HOP_LE = ("localhost", "127.0.0.1", "[::1]")

# Khi chạy `npm run dev`, giao diện nằm ở cổng 5173 nên là "nguồn khác" với API.
# Trình duyệt sẽ chặn nếu máy chủ không cho phép. Chỉ bật khi có tham số --dev.
NGUON_DEV = "http://localhost:5173"

# =============================================================================
# 2. THƯ MỤC
# =============================================================================
THU_MUC_WEB = "web/dist"     # Giao diện React đã build (npm run build)
THU_MUC_OUTPUT = "output"    # Nơi chứa file kết quả — chỉ tải về được từ đây

# =============================================================================
# 3. GIỚI HẠN
# =============================================================================
# Số dòng log giữ lại cho mỗi việc. Giữ hết 7.000 dòng của một lần chạy Suggest
# sẽ làm trình duyệt ì ạch, mà người dùng cũng không đọc lại quá xa.
SO_DONG_LOG_GIU = 1500

# Số việc cũ giữ trong bộ nhớ. Quá số này thì việc cũ nhất bị dọn đi.
SO_VIEC_GIU = 12

# Kích thước tối đa của một yêu cầu POST (bài viết + prompt có thể khá dài).
KICH_THUOC_POST_TOI_DA = 4 * 1024 * 1024   # 4 MB

# Nhịp gửi tín hiệu giữ kết nối SSE, tính bằng giây. Nếu không gửi gì suốt
# nhiều phút (lúc Suggest đang nghỉ chống chặn), proxy hoặc trình duyệt có thể
# tự cắt kết nối.
NHIP_GIU_KET_NOI = 15

# =============================================================================
# 4. TÙY CHỌN HIỆN TRÊN GIAO DIỆN
# =============================================================================
# Khung thời gian của Google Trends. Khóa là giá trị gửi cho Google.
KHUNG_THOI_GIAN = [
    ("now 7-d", "7 ngày qua"),
    ("today 1-m", "30 ngày qua (mặc định)"),
    ("today 3-m", "3 tháng qua"),
    ("today 12-m", "12 tháng qua"),
]

# Khu vực. Google dùng mã ISO, VN-SG là TP.HCM.
KHU_VUC = [
    ("VN", "Toàn quốc"),
    ("VN-SG", "TP. Hồ Chí Minh"),
    ("VN-HN", "Hà Nội"),
]
