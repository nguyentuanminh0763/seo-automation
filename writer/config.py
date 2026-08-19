# -*- coding: utf-8 -*-
"""
Hằng số của công cụ viết bài.

Lưu ý khác với hai công cụ kia: những thứ bạn sửa thường xuyên (API key,
chọn nhà cung cấp, model) nằm ở file .env chứ KHÔNG nằm ở đây, vì .env
không bị đẩy lên GitHub còn file này thì có.
"""

# =============================================================================
# 1. THƯ MỤC
# =============================================================================
THU_MUC_PROMPT = "prompts"      # Nơi chứa các file prompt bạn tự viết
THU_MUC_OUTPUT = "output"       # Nơi lưu bài viết đã tạo
DUOI_FILE_PROMPT = ".md"

# Chuỗi này trong file prompt sẽ được thay bằng từ khóa bạn chọn.
CHO_CHEN_TU_KHOA = "{keyword}"

# =============================================================================
# 2. MẶC ĐỊNH (bị .env ghi đè nếu .env có khai báo)
# =============================================================================
NHA_CUNG_CAP_MAC_DINH = "gemini"
GEMINI_MODEL_MAC_DINH = "gemini-3.6-flash"
CLAUDE_MODEL_MAC_DINH = "claude-opus-5"
MAX_TOKENS_MAC_DINH = 8000
TIMEOUT_MAC_DINH = 180

# =============================================================================
# 3. BẢNG GIÁ (USD cho 1 triệu token) — để ước tính chi phí hiển thị
# =============================================================================
# Gemini gói miễn phí không tính tiền -> để 0.
BANG_GIA = {
    "gemini": {"vao": 0.0, "ra": 0.0},
    "claude-opus-5": {"vao": 5.0, "ra": 25.0},
    "claude-sonnet-5": {"vao": 3.0, "ra": 15.0},
    "claude-haiku-4-5": {"vao": 1.0, "ra": 5.0},
}

# Tỷ giá quy đổi để hiển thị cho dễ hình dung. Chỉ là ước tính.
TY_GIA_VND = 26000

# =============================================================================
# 4. ĐẦU RA
# =============================================================================
OUTPUT_PREFIX = "baiviet"

# Câu người dùng cần thay bằng số liệu thật trước khi đăng.
# Công cụ sẽ đếm và cảnh báo nếu bài còn sót chỗ chưa điền.
DAU_HIEU_CAN_BO_SUNG = "[CẦN BỔ SUNG"
