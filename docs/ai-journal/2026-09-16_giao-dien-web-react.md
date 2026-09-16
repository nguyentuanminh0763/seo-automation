# Giao diện web React cho hai công cụ thu thập

**Ngày:** 2026-09-16
**Giai đoạn:** 1c — Giao diện web
**Trạng thái:** ✅ Đã chạy thật bằng trình duyệt — 48 phép thử đạt. ⚠️ **Chưa gọi Google lần nào.**

---

## Bối cảnh

Người dùng yêu cầu: *"dựng 1 FE REACT JS cho dự án này để tôi có thể trải nghiệm giao diện
chuyên nghiệp hơn"*, và yêu cầu **trình bày kiến trúc trước để duyệt** thay vì làm ngay.

Đây là lần thứ hai luật dự án bị đảo vì yêu cầu của người dùng. Lần đầu là "giao diện web"
ngày 2026-08-19 (đảo xong nhưng làm bằng tkinter). Lần này là **"không dùng framework nặng"**.

---

## Vấn đề cốt lõi phải giải trước khi viết dòng code nào

React chạy trong trình duyệt. Trình duyệt **không gọi được** `pytrends`, `pandas`, hay đọc
file `.env` trên máy. Nên "dựng FE React" một cách độc lập là bất khả thi — bắt buộc phải có
một tầng máy chủ làm cầu nối.

```
Trình duyệt (React)  ⇄ HTTP + SSE ⇄  webapi/ (FastAPI)  →  trends/ · suggest/  (GIỮ NGUYÊN)
```

`webapi/` không chứa một dòng logic thu thập nào, đúng như `gui/` đang làm.
**Ba package lõi không bị sửa một chữ.**

---

## Bốn quyết định đã trình người dùng chốt

| Câu hỏi | Tôi đề xuất | Người dùng chốt |
|---|---|---|
| Máy chủ viết bằng gì | Thư viện chuẩn Python (0 phụ thuộc mới) | **FastAPI + uvicorn** |
| Cách khởi động | Commit sẵn bản build | **Commit sẵn bản build** ✓ |
| Giao diện tkinter cũ | Giữ nguyên, chạy song song | **Giữ nguyên** ✓ |
| Phạm vi | Đủ 4 màn hình | **Chỉ 2 màn thu thập trước** |

Người dùng chọn FastAPI dù tôi nghiêng về thư viện chuẩn. Đánh đổi đã nói rõ trước khi chốt:
thêm phụ thuộc phải cài trên máy không có Python trong PATH, đổi lại được kiểm tra dữ liệu
đầu vào tự động và tài liệu API tự sinh tại `/docs`. Đã ghi ngoại lệ vào `CLAUDE_RULES.md`
kèm ranh giới rõ: **chỉ `webapi/` và `web/`**, ba package lõi vẫn phải chạy được bằng dòng
lệnh mà không cần FastAPI.

---

## Ba chỗ khó về kỹ thuật

### 1. Suggest chạy 13 phút — không nhét vừa một yêu cầu HTTP

Trình duyệt, proxy và mọi thiết bị trên đường đi đều tự cắt kết nối trước đó rất lâu.

Cách giải: yêu cầu chạy chỉ **tạo việc rồi trả về mã số ngay**. Tiến trình đi qua một kênh
SSE riêng. Hệ quả tốt ngoài dự tính: **đóng tab không làm dừng lần chạy**, mở lại tab là
thấy tiếp — thứ bản tkinter không làm được.

Một bẫy đã tránh: hàm sinh sự kiện SSE khai bằng `def` chứ không phải `async def`. Nó đọc
hàng đợi bằng lệnh chờ; viết thành `async def` sẽ khóa chết vòng lặp sự kiện của uvicorn và
**mọi yêu cầu khác treo theo**.

### 2. Chống chặn IP

Trends và Suggest dùng **chung một khóa** trong `webapi/jobs.py`. Chạy song song = gấp đôi
lượt hỏi Google từ cùng một IP, đúng thứ `CLAUDE_RULES.md` cấm. Yêu cầu thứ hai bị trả về
409 kèm câu giải thích tiếng Việt, không phải mã lỗi trống trơn.

### 3. Web thì ai mở trình duyệt cũng vào được

Ba chốt: chỉ nghe `127.0.0.1`; chặn header `Host` lạ (DNS rebinding); không bật CORS trừ khi
chạy `--dev`. Đường dẫn tải file kiểm tra file phải nằm trong `output/` — không có chốt đó
thì `../../.env` lôi được API key ra ngoài. Đã thử 3 kiểu đường dẫn lạ, chặn hết.

---

## Một cái bẫy thật phát hiện được nhờ việc này

`.gitignore` có luật `_*.py` để chặn file nháp (`_t3.py` từng lọt vào vùng chờ commit).
Luật đó **khớp luôn `__init__.py`**. Các package cũ (`trends/`, `gui/`...) thoát vì đã được
commit trước khi luật ra đời — nhưng **package mới thì `__init__.py` im lặng biến mất**,
và lỗi chỉ lộ ra khi người khác clone repo về chạy.

Đã vá bằng dòng `!__init__.py`.

---

## Kiểm chứng

**48 phép thử, không gọi Google lần nào.**

| Nhóm | Số phép | Cách làm |
|---|---:|---|
| Backend | 27 | `TestClient` chạy qua đúng ứng dụng FastAPI thật, thay hàm quét bằng bản giả |
| Giao diện | 21 | Playwright điều khiển Chromium thật, bấm đúng các nút người dùng sẽ bấm |

Những thứ đã kiểm được bằng chạy thật:

- Log chảy về giao diện theo thời gian thực qua SSE
- Bấm Dừng giữa chừng → trạng thái `da_dung`, **giữ nguyên 90 dòng đã thu**
- Xuất Excel → đọc lại bằng `pandas`, đúng số dòng, **tiếng Việt không vỡ**
- Tải file về từ trình duyệt thật
- Chặn 3 kiểu đường dẫn lạ, chặn Host lạ (HTTP 400)
- Việc thứ hai bị chặn bằng 409
- Lỗi giữa chừng (giả lập Google trả 429) không làm sập máy chủ
- Sắp xếp cột số theo **giá trị** chứ không theo chữ cái (87.100 phải trên 9.000)
- Ước tính Suggest lấy từ máy chủ: 24 từ × 45 biến thể = 1.080 lượt — khớp
  `suggest/settings.py`. Cố ý không nhân lại trong giao diện, chép công thức sang là sớm
  muộn lệch
- Nền tối/sáng, nhớ lựa chọn sau khi tải lại trang
- Màn hình điện thoại 430px không tràn ngang
- Không có lỗi JavaScript nào

---

## ⚠️ Chưa kiểm được — việc đầu tiên của phiên sau

**Chưa lần nào gọi Google thật qua giao diện web.** Toàn bộ 48 phép thử dùng dữ liệu giả,
cố ý: gọi thật nhiều lần trong lúc phát triển là cách nhanh nhất để bị chặn IP vài giờ.

Phần chưa chắc chắn: `quet_breakout()` và `thu_thap()` chạy qua `webapi/runners.py` với
`nen_dung` là hàm của lớp `Viec` thay vì của `LuongChay`. Chữ ký hàm giống hệt nhau và đã
chạy đúng với bản giả, nhưng **theo luật dự án, chưa gọi API thật thì chưa được coi là xong.**

Việc cần làm: mở giao diện web, chạy Trends với 5 từ khóa, xem có ra dòng nào không.
Một lần là đủ kết luận.

---

## File đã tạo

```
webapi/          7 file — API (config, log_bridge, jobs, runners, serializers, routes, server)
web/src/        11 file — giao diện React
web/dist/        3 file — bản build, commit cố ý
seo_web.py              — điểm chạy
Chay_giao_dien_web.bat  — bấm đúp để chạy
```

Sửa: `.gitignore` (vá bẫy `__init__.py`), `requirements.txt`, `CLAUDE_RULES.md`,
`README.md`, `PROJECT_STATE.md`, `implementation_plan.md`.
