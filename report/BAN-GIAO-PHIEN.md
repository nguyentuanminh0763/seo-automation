# Prompt bàn giao sang phiên mới

Copy toàn bộ khối dưới đây, dán vào đầu cửa sổ Claude Code mới.
Cập nhật lần cuối: 2026-08-20.

---

```
Tiếp tục dự án SEO Automation cho giaphongpc.vn tại C:\Users\PC\Desktop\seo

Đọc trước khi làm gì: CLAUDE.md → PROJECT_STATE.md → docs/RESULTS_LOG.md

TÔI KHÔNG BIẾT LẬP TRÌNH. Trả lời tiếng Việt, đưa lệnh copy-paste được ngay.

=== ĐANG CÓ GÌ ===
3 công cụ, chạy bằng cách bấm đúp Chay_giao_dien.bat (giao diện 3 tab):
1. trends/  — Google Trends, bắt từ khóa Breakout
2. suggest/ — Google Suggest, đã thu 7.045 từ khóa
3. writer/  — viết bài bằng AI + tự kiểm tra SEO bằng code

Đang dùng OpenAI gpt-5-mini (đổi trong nút "Cấu hình AI" ngay trong app,
không sửa .env bằng tay nữa). Còn hỗ trợ Gemini (free) và Claude.

=== ĐANG DANG DỞ, THEO THỨ TỰ ƯU TIÊN ===
1. Chưa viết thử bài nào bằng OpenAI gpt-5-mini — cần chạy 1 bài xác nhận.
2. Chạy 3 bài thử thì cả 3 đều thiếu external link và thiếu từ khóa ở kết
   luận. Đã siết lời dặn trong prompts/giaphongpc-tong-quat.md nhưng CHƯA
   chạy lại để xác nhận đã hết.
3. Nút "Copy để dán WordPress" chưa test trên WordPress thật.
4. Chuẩn mật độ từ khóa 0,40–0,55% trong writer/config.py có thể quá chặt —
   từ khóa ngắn là chủ đề chính của bài luôn vượt ngưỡng này.

=== VIỆC ĐANG BÀN DỞ (quan trọng nhất) ===
Tôi có 7.045 từ khóa nhưng KHÔNG có cột nào để xếp thứ tự ưu tiên viết bài.

Một SEO engineer cùng công ty dùng Ahrefs xuất từ khóa của đối thủ hacom.vn
ra Google Sheet, rồi lọc theo: Traffic Potential cao + KD thấp (0–3) +
đối thủ đang xếp hạng kém (vị trí 14–52). Bài học rút ra: dân SEO có nghề
chọn theo Traffic Potential chứ không theo Volume, vì volume của một cụm
chính xác luôn đánh giá thấp cả chủ đề.

Kế hoạch: làm tab thứ 4 đọc file xuất từ Ahrefs hoặc Google Search Console,
nối Traffic Potential + KD + vị trí vào 7.045 từ khóa của tôi, rồi nối
thẳng sang tab Viết bài. Chưa có file dữ liệu — tôi sẽ đi xin.

=== LUẬT BẮT BUỘC ===
- Python KHÔNG có trong PATH:
  C:\Users\PC\AppData\Local\Programs\Python\Python312\python.exe
- Git dùng remote HTTPS (khóa SSH trên máy thuộc tài khoản khác).
- output/ và .env KHÔNG BAO GIỜ commit — repo public.
- Commit tiếng Anh, chuẩn Conventional Commits (feat:/fix:/docs:).
- Luồng nền KHÔNG được gọi hàm tkinter nào, kể cả after().
- Đếm số liệu bài viết bằng CODE, không hỏi AI — nó đếm sai 50–60%.
- CHẠY THẬT rồi mới báo xong. Dự án này đã có hơn 15 lỗi chỉ lộ ra khi chạy.
  Chạy xong không báo lỗi mới là BẮT ĐẦU kiểm chứng, chưa phải kết thúc.
```

---

## Ghi chú thêm cho tôi (không cần dán)

**Gemini free:** 20 lượt/ngày cho MỖI model. Hết thì đổi model là có hạn mức
mới — xoay vòng 5 model được ~100 lượt/ngày.

**2 skill nháp** đang ở `C:\Users\PC\.claude\skills\` (`windows-desktop-tool`
và `project-handoff-docs`), đã viết sẵn đề bài trong `evals/evals.json` nhưng
chưa chạy thử. Thư mục đó nằm ngoài repo nên chưa được sao lưu.

**Repo:** https://github.com/nguyentuanminh0763/seo-automation
