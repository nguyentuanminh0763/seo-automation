# CLAUDE.md

Dự án: **SEO Automation cho giaphongpc.vn** — hai công cụ Python thu thập từ khóa SEO.

## Đọc trước khi làm bất cứ việc gì

1. [`CLAUDE_RULES.md`](CLAUDE_RULES.md) — luật làm việc, các bẫy kỹ thuật đã gặp thật
2. [`PROJECT_STATE.md`](PROJECT_STATE.md) — hiện trạng, vấn đề đang tồn tại
3. [`SEO_AI_WORKFLOW_GUIDE.md`](SEO_AI_WORKFLOW_GUIDE.md) — cấu trúc dự án, quy trình chuẩn
4. [`docs/RESULTS_LOG.md`](docs/RESULTS_LOG.md) — kết quả các lần chạy trước

## Nhắc nhanh

- Người dùng **không biết lập trình**. Trả lời bằng tiếng Việt, đưa lệnh copy-paste được ngay.
- Python **không nằm trong PATH**: `C:\Users\PC\AppData\Local\Programs\Python\Python312\python.exe`
- Git phải dùng remote **HTTPS** (khóa SSH trên máy thuộc tài khoản khác, không có quyền ghi).
- Thư mục `output/` **không bao giờ commit** — repo public, đó là dữ liệu kinh doanh.
- **Không báo "đã xong" khi chưa chạy thật.** Dự án này đã có 3 lỗi chỉ lộ ra khi chạy.

## Sau khi thay đổi

Cập nhật `PROJECT_STATE.md`, thêm nhật ký vào `docs/ai-journal/`, ghi số liệu vào
`docs/RESULTS_LOG.md` nếu có chạy công cụ.
