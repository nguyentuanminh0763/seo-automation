# -*- coding: utf-8 -*-
"""
CẤU HÌNH CÔNG CỤ LẤY KEYWORD LÀM CONTENT - FILE DUY NHẤT BẠN CẦN SỬA.

Toàn bộ file này chỉ chứa hằng số, không có logic. Sửa thoải mái không sợ vỡ code.
"""

# =============================================================================
# 1. TỪ KHÓA GỐC - CHỦ ĐỀ BẠN MUỐN VIẾT BÀI
# =============================================================================
# Khác với công cụ Trends: ở đây nên dùng từ NGẮN VÀ RỘNG (vd "máy tính", "cpu"),
# vì công cụ sẽ tự ghép thêm hàng chục biến thể để moi ra câu hỏi dài.
# Từ càng rộng -> càng ra nhiều ý tưởng bài viết.
SEED_KEYWORDS = [
    # --- Máy tính bộ ---
    "máy tính",
    "máy tính bàn",
    "pc gaming",
    "build pc",
    "máy tính cũ",
    # --- Laptop ---
    "laptop",
    "laptop gaming",
    "laptop cũ",
    # --- Linh kiện ---
    "cpu",
    "cpu hàng tray",
    "card màn hình",
    "rtx 5060",
    "ram máy tính",
    "ổ cứng ssd",
    "mainboard",
    "tản nhiệt",
    # --- Màn hình ---
    "màn hình máy tính",
    "màn hình 2k",
    # --- Gaming gear ---
    "chuột máy tính",
    "bàn phím cơ",
    # --- Phần mềm / Lỗi thường gặp (rất hợp làm bài kéo traffic) ---
    "windows 11",
    "giả lập",
    # --- Dịch vụ ---
    "sửa máy tính",
    "thu mua pc cũ",
]

# =============================================================================
# 2. TỪ MỒI - BÍ QUYẾT MOI RA CÂU HỎI DÀI
# =============================================================================
# Nguyên lý: ghép từ mồi vào TRƯỚC hoặc SAU từ gốc rồi hỏi Google gợi ý.
# Ví dụ: "cách" + "máy tính" -> Google gợi ý "cách kiểm tra ram máy tính đơn giản"

# Ghép vào TRƯỚC từ gốc
TU_MOI_TRUOC = [
    "cách",
    "tại sao",
    "có nên",
    "hướng dẫn",
    "so sánh",
    "review",
    "mua",
    "nơi bán",
    "địa chỉ bán",
    "top",
]

# Ghép vào SAU từ gốc
TU_MOI_SAU = [
    "là gì",
    "giá bao nhiêu",
    "loại nào tốt",
    "ở đâu",
    "cho sinh viên",
    "giá rẻ",
    "cũ",
    "bị lỗi",
    "khắc phục",
    "trả góp",
    "nên mua",
    "2026",
]

# Ghép từng chữ cái a-z vào sau từ gốc (mẹo kinh điển của dân SEO).
# Bật lên sẽ ra nhiều keyword hơn hẳn nhưng chạy lâu hơn ~3 lần.
DUNG_BANG_CHU_CAI = True
BANG_CHU_CAI = "abcdefghiklmnoprstuvxy"  # bỏ các chữ hiếm dùng trong tiếng Việt

# =============================================================================
# 3. THÔNG SỐ KẾT NỐI GOOGLE SUGGEST
# =============================================================================
HL = "vi"       # Ngôn ngữ
GL = "vn"       # Quốc gia
CLIENT = "firefox"          # Kiểu dữ liệu trả về. Đừng đổi trừ khi biết rõ.
REQUEST_TIMEOUT = 10        # Giây

# =============================================================================
# 4. CHỐNG CHẶN IP
# =============================================================================
# Google Suggest dễ tính hơn Google Trends rất nhiều nên độ trễ có thể ngắn.
DELAY_MIN = 0.3             # Nghỉ tối thiểu giữa 2 lượt hỏi (giây)
DELAY_MAX = 0.9             # Nghỉ tối đa (giây)
MAX_RETRIES = 3             # Số lần thử lại khi lỗi
COOLDOWN_ON_BLOCK = 20      # Bị chặn -> ngủ 20s, lần sau 40s, 60s...

PROXY_LIST = [
    # "http://123.45.67.89:8080",
]

# =============================================================================
# 5. PHÂN LOẠI Ý ĐỊNH TÌM KIẾM
# =============================================================================
# Công cụ đọc từng keyword, dò xem chứa dấu hiệu nào thì xếp vào nhóm đó.
# THỨ TỰ TRONG DANH SÁCH LÀ THỨ TỰ ƯU TIÊN - nhóm ở trên được kiểm tra trước.
LUAT_PHAN_LOAI = [
    (
        "Khắc phục lỗi",
        "Bài hướng dẫn sửa lỗi",
        ["lỗi", "khắc phục", "sửa", "fix", "hỏng", "treo", "đơ", "lag", "giật",
         "tụt fps", "chậm", "nóng", "không vào được", "không nhận", "không lên",
         "không hiện", "không chạy", "bị đầy", "kêu to", "sập nguồn"],
    ),
    (
        "Khái niệm",
        "Bài giải thích thuật ngữ",
        ["là gì", "nghĩa là", "viết tắt", "có nghĩa", "khác gì"],
    ),
    (
        "So sánh - Tư vấn",
        "Bài so sánh / tư vấn chọn mua",
        ["so sánh", " vs ", "khác nhau", "nào tốt", "loại nào", "có nên",
         "nên mua", "đáng mua", "hay hơn", "top ", "tốt nhất", "review"],
    ),
    (
        "Thương mại",
        "Trang bán hàng / danh mục",
        ["giá", "bao nhiêu", "mua", "bán", "ở đâu", "uy tín", "trả góp",
         "giá rẻ", "thanh lý", "khuyến mãi", "giảm giá", "cũ", "second hand"],
    ),
    (
        "Hướng dẫn",
        "Bài hướng dẫn từng bước",
        ["cách", "hướng dẫn", "làm sao", "làm thế nào", "cài", "tải",
         "kiểm tra", "chỉnh", "nâng cấp", "vệ sinh", "lắp", "test"],
    ),
]

# Nhóm mặc định khi không khớp luật nào ở trên.
NHOM_MAC_DINH = ("Thông tin sản phẩm", "Trang sản phẩm / danh mục")

# =============================================================================
# 6. BỘ LỌC RÁC
# =============================================================================
DO_DAI_TOI_THIEU = 2        # Bỏ keyword ngắn hơn N từ (quá chung chung)
# Bỏ keyword chứa các từ này (không liên quan mảng máy tính của bạn)
TU_KHOA_LOAI_BO = [
    # --- Mạng xã hội / sàn TMĐT ---
    "tiktok", "facebook", "zalo", "shopee", "lazada",
    # --- Thiết bị khác ---
    "iphone", "android", "điện thoại", "samsung galaxy",
    "máy ảnh", "tivi", "tủ lạnh", "máy giặt",
    # --- BẪY TIẾNG VIỆT: "máy tính" còn có nghĩa là MÁY TÍNH CẦM TAY (calculator) ---
    # Không lọc thì Google trả về đầy "sửa máy tính casio 570", "máy tính fx-580"...
    # hoàn toàn không liên quan mảng PC. Đã đo thực tế: chiếm ~1,3% kết quả.
    "casio", "cầm tay", "bỏ túi", "fx-570", "fx-580", "fx 570", "fx 580",
    "570vn", "580vn", "casio 880", "vinacal",
]

# =============================================================================
# 7. ĐẦU RA
# =============================================================================
OUTPUT_DIR = "output"
OUTPUT_PREFIX = "content_keywords_giaphongpc"
