# -*- coding: utf-8 -*-
"""
CẤU HÌNH MẶC ĐỊNH - ĐÂY LÀ FILE DUY NHẤT BẠN CẦN SỬA HÀNG NGÀY.

Toàn bộ file này chỉ chứa hằng số, không có logic. Sửa thoải mái không sợ vỡ code.
Các giá trị ở đây là MẶC ĐỊNH; tham số dòng lệnh (--geo, --timeframe...) sẽ ghi đè lên.
"""

# =============================================================================
# 1. DANH SÁCH TỪ KHÓA HẠT GIỐNG CỦA GIA PHONG PC
# =============================================================================
# Mẹo: giữ từ khóa ngắn, KHÔNG DẤU (người Việt gõ không dấu nhiều hơn),
# và bám sát nhóm sản phẩm đang bán. Xóa/thêm dòng thoải mái.
SEED_KEYWORDS = [
    # --- Card màn hình / Linh kiện nóng ---
    "rtx 5060 ti",
    "rtx 5060",
    "cpu hang tray",
    "tan nhiet nuoc",
    "ram ddr5",
    "mainboard b760",
    # --- Máy tính bộ / Build PC ---
    "build pc",
    "pc gaming",
    "pc gia lap",
    "pc do hoa",
    "may tinh bo cu",
    # --- Laptop ---
    "laptop gaming",
    "laptop van phong",
    "laptop cu gia re",
    # --- Màn hình ---
    "man hinh 2k",
    "man hinh cong gaming",
    "man hinh 144hz",
    # --- Dịch vụ / Long-tail có ý định mua cao ---
    "thu mua pc cu",
    "sua may tinh tphcm",
    "loi windows 11",
]

# =============================================================================
# 2. THÔNG SỐ KẾT NỐI GOOGLE TRENDS
# =============================================================================
HL = "vi-VN"            # Ngôn ngữ trả về (đổi 'en-US' nếu gặp lỗi encoding)
TZ = -420               # Múi giờ tính bằng phút. VN = UTC+7 -> -420
GEO = "VN"              # Khu vực. Có thể đổi 'VN-SG' (TP.HCM), 'VN-HN' (Hà Nội)
TIMEFRAME = "today 1-m"  # 30 ngày qua. Khác: 'today 3-m', 'today 12-m', 'now 7-d'
CATEGORY = 0            # 0 = tất cả danh mục. (5 = Computers & Electronics)
GPROP = ""              # "" = Web Search. Khác: 'images', 'news', 'youtube', 'froogle'

# =============================================================================
# 3. CHỐNG CHẶN IP (RATE LIMITING / ANTI-BAN)
# =============================================================================
BATCH_SIZE = 5              # RÀNG BUỘC CỨNG của Google: tối đa 5 từ khóa / payload
SLEEP_MIN = 5               # Nghỉ ngẫu nhiên tối thiểu giữa 2 nhóm (giây)
SLEEP_MAX = 12              # Nghỉ ngẫu nhiên tối đa giữa 2 nhóm (giây)
MAX_RETRIES = 3             # Số lần thử lại cho mỗi nhóm khi gặp lỗi
COOLDOWN_ON_BLOCK = 60      # Bị chặn -> ngủ 60s, lần sau 120s, 180s... (lũy tiến)
REQUEST_TIMEOUT = (10, 30)  # (timeout kết nối, timeout đọc) tính bằng giây

# =============================================================================
# 4. PROXY (DỰ PHÒNG CHO QUY MÔ LỚN)
# =============================================================================
# Để trống [] nếu chạy bằng IP nhà. Khi quét nhiều seed thì nên điền proxy.
# Định dạng bắt buộc của pytrends: 'https://user:pass@ip:port' hoặc 'https://ip:port'
PROXY_LIST = [
    # "https://123.45.67.89:8080",
    # "https://user:pass@111.22.33.44:3128",
]

# =============================================================================
# 5. NGƯỠNG LỌC
# =============================================================================
# Google gắn nhãn 'Breakout' cho từ khóa tăng > 5000%.
BREAKOUT_THRESHOLD = 5000   # Từ mức này trở lên được tính là Breakout
RISING_THRESHOLD = 500      # Ngưỡng cho chế độ --include-rising (lấy thêm từ tăng mạnh)

# =============================================================================
# 6. ĐẦU RA
# =============================================================================
OUTPUT_DIR = "output"                   # Thư mục báo cáo (tự tạo nếu chưa có)
OUTPUT_PREFIX = "breakout_giaphongpc"   # Tiền tố tên file
