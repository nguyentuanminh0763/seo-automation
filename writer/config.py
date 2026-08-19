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

# Gói Gemini miễn phí giới hạn ~20 lượt/NGÀY cho MỖI model. Hết model này thì
# các model khác vẫn còn nguyên hạn mức, nên khi bị chặn, công cụ sẽ thử lần
# lượt danh sách dưới đây và gợi ý model còn dùng được.
# Xếp theo thứ tự ưu tiên về chất lượng.
MODEL_DU_PHONG = [
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-flash-latest",
    "gemini-3.1-flash-lite",
]
CLAUDE_MODEL_MAC_DINH = "claude-opus-5"
OPENAI_MODEL_MAC_DINH = "gpt-5"
MAX_TOKENS_MAC_DINH = 24000
TIMEOUT_MAC_DINH = 420

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

# Ba nhà cung cấp được hỗ trợ. Tên hiển thị dùng cho ô chọn trên giao diện.
NHA_CUNG_CAP = {
    "gemini": {
        "ten": "Google Gemini",
        "ghi_chu": "Có gói miễn phí ~20 lượt/ngày mỗi model, không cần thẻ",
        "khoa_env": "GEMINI_API_KEY",
        "model_env": "GEMINI_MODEL",
        "lay_key": "https://aistudio.google.com/apikey",
        "dang_key": "AIza...",
    },
    "openai": {
        "ten": "OpenAI",
        "ghi_chu": "Trả phí theo lượng dùng, cần nạp số dư trước",
        "khoa_env": "OPENAI_API_KEY",
        "model_env": "OPENAI_MODEL",
        "lay_key": "https://platform.openai.com/api-keys",
        "dang_key": "sk-...",
    },
    "claude": {
        "ten": "Anthropic Claude",
        "ghi_chu": "Trả phí, văn phong tự nhiên nhất",
        "khoa_env": "ANTHROPIC_API_KEY",
        "model_env": "CLAUDE_MODEL",
        "lay_key": "https://console.anthropic.com",
        "dang_key": "sk-ant-...",
    },
}

# Tỷ giá quy đổi để hiển thị cho dễ hình dung. Chỉ là ước tính.
TY_GIA_VND = 26000

# =============================================================================
# 4. CHUẨN KIỂM TRA SEO
# =============================================================================
# Tool tự ĐẾM những con số này bằng code, không hỏi AI.
# Lý do: mô hình ngôn ngữ không đếm được. Đo thực tế trên một bài, AI tự khai
# 3.682 từ / 17 lần từ khóa trong khi số thật là 5.876 từ / 26 lần — sai 50–60%
# nhưng bảng trông rất thuyết phục. Sửa số ở đây nếu bạn đổi chuẩn.

CHUAN_SEO = {
    "so_tu_toi_thieu": 3000,
    "so_tu_toi_da": 4000,
    "so_h1": 1,
    "so_h2_toi_thieu": 8,
    "so_h2_toi_da": 12,
    "tu_khoa_min": 15,
    "tu_khoa_max": 20,
    "mat_do_min": 0.40,          # phần trăm
    "mat_do_max": 0.55,
    "h2_chua_tu_khoa_min": 3,
    "title_toi_da": 60,          # ký tự
    "meta_min": 140,
    "meta_max": 158,
    "internal_min": 5,
    "internal_max": 8,
    "external_min": 1,
    "external_max": 2,
    "so_anh_toi_thieu": 4,
    "so_faq_toi_thieu": 5,
}

# Tên miền của bạn — dùng để phân biệt internal link với external link.
TEN_MIEN = "giaphongpc.vn"

# Dấu hiệu nhận biết các khối bắt buộc trong bài.
DAU_HIEU = {
    "tra_loi_nhanh": r"trả lời nhanh",
    "faq": r"^#{2,3}\s*.*(FAQ|câu hỏi thường gặp)",
    "checklist": r"checklist|tự kiểm tra",
    "author_bio": r"đội ngũ|tác giả|author",
    "ngay_cap_nhat": r"cập nhật",
    "canh_bao_an_toan": r"an toàn|ngắt điện|rút nguồn|điện giật",
    "gioi_han": r"tham khảo|không nên tự|khuyến cáo",
    "anh": r"\[ẢNH",
}

# Số điện thoại / thông tin NAP cần có mặt. Sửa cho khớp doanh nghiệp của bạn.
NAP_CAN_CO = ["0706.992.233"]

# =============================================================================
# 5. ĐẦU RA
# =============================================================================
OUTPUT_PREFIX = "baiviet"

# Câu người dùng cần thay bằng số liệu thật trước khi đăng.
# Công cụ sẽ đếm và cảnh báo nếu bài còn sót chỗ chưa điền.
DAU_HIEU_CAN_BO_SUNG = "[CẦN BỔ SUNG"
