# SEO Automation — Project State

> **Cập nhật lần cuối:** 2026-08-20 (Chạy thật bằng OpenAI gpt-5-mini, sửa lỗi mất thẻ H2)
> **Trạng thái tổng thể:** ✅ Cả hai công cụ đã chạy thật, ra kết quả thật, đã đẩy lên GitHub

---

## Nhận diện dự án

| Mục | Giá trị |
|---|---|
| Tên | SEO Automation — giaphongpc.vn |
| Repo | https://github.com/nguyentuanminh0763/seo-automation (public) |
| Ngôn ngữ | Python 3.12.10 |
| Thư viện chính | pytrends 4.9.2, pandas 3.0.5, requests 2.34.2, openpyxl 3.1.5 |
| Nền tảng | Windows 11 |
| Người dùng | Không biết lập trình — mọi hướng dẫn phải bằng tiếng Việt |

---

## Hiện trạng — hai công cụ đã hoàn thành

| Công cụ | Nguồn dữ liệu | Trạng thái | Sản lượng thực đo |
|---|---|---|---|
| `trends_scrapper.py` | Google Trends | ✅ Chạy được | 7 từ khóa Breakout / 53 giây |
| `suggest_scrapper.py` | Google Suggest | ✅ Chạy được | 7.045 từ khóa / 13,3 phút |

Chi tiết từng lần chạy: [`docs/RESULTS_LOG.md`](docs/RESULTS_LOG.md)

---

## Cập nhật mới nhất — Chạy thật bằng OpenAI, sửa lỗi mất thẻ H2 (2026-08-20)

**File đã sửa:** `prompts/giaphongpc-tong-quat.md`

**Đã làm:** viết thật 2 bài bằng `gpt-5-mini` và chấm bằng `writer/auditor.py`.
Số liệu đầy đủ trong [`docs/RESULTS_LOG.md`](docs/RESULTS_LOG.md).

**Lỗi thật đã phát hiện — nghiêm trọng nhất từ trước tới nay về mặt SEO:**

`gpt-5-mini` **không tự dùng cú pháp `##`**. Nó viết tên mục thành dòng chữ trơn, nên bài
xuất ra HTML có **0 thẻ H2**. Bài đọc vẫn xuôi nên nhìn qua không thấy gì sai — chỉ bộ đếm
bằng code mới lộ ra. Nếu đăng lên WordPress thì đó là một bài không có cấu trúc heading,
gần như vô giá trị SEO.

Nguyên nhân: prompt chỉ nói "bài viết dạng Markdown" và ghi "Thẻ H2: 8–12" trong bảng mục
tiêu, không hề chỉ rõ cú pháp. Gemini tự suy ra được, gpt-5-mini thì không. Câu
"Không dùng dấu `#` cho hai dòng mốc PHẦN 1 / PHẦN 2" nhiều khả năng còn bị hiểu rộng ra
thành "đừng dùng `#`".

Cách sửa: thêm vào PHẦN 2 của prompt một bảng cú pháp heading bắt buộc và một khung bài mẫu
dạng khối code, kèm ghi chú rằng ngoại lệ `#` chỉ áp dụng cho đúng hai dòng mốc.
Chạy lại: **0 H2 → 11 H2**, **0 FAQ → 5 FAQ**, số mục chưa đạt từ 8 xuống 5.

**Đã xác nhận hết lỗi (mục tồn của phiên trước):** external link ✅ và từ khóa ở kết bài ✅
đều đạt ở cả hai bài. Lời dặn siết thêm hôm 2026-08-20 đã ăn.

---

## Cập nhật trước đó — Kiểm tra SEO, OpenAI, màn hình cấu hình (2026-08-20)

**File mới:** `writer/auditor.py`, `gui/audit_window.py`, `gui/settings_window.py`,
`prompts/giaphongpc-tong-quat.md`, `prompts/giaphongpc-suachua.md`

**Đã làm:**
- **Bộ đếm SEO bằng code** thay cho bảng AI tự khai. Đo thật: AI khai 3.682 từ /
  17 lần từ khóa trong khi số thật là 5.876 / 26 — sai 50–60%.
- **Prompt tự nhận diện ý định** từ khóa (6 nhóm A–F) rồi chọn khung bài. Đúng 4/4 khi thử.
- **Thêm nhà cung cấp OpenAI** (REST, không cần thư viện mới).
- **Màn hình Cấu hình AI** — nhập key, chọn model, kiểm tra kết nối ngay trong app,
  không phải sửa `.env` bằng tay nữa.

**Lỗi đã phát hiện và sửa (tất cả đều của tôi, chỉ lộ khi chạy thật):**

| Lỗi | Hậu quả |
|---|---|
| `<[^>]+>` khớp dấu `<` trong "Delta E < 2" | Nuốt 75% bài viết khi đếm |
| Xóa nguyên dòng bảng | Bài về giá/so sánh mất phần lớn nội dung |
| Đếm từ và đếm từ khóa khác cơ sở | Mật độ ra 6,17% thay vì 1,18% |
| `NFD` không tách được chữ `đ` | Mọi từ khóa có `đ` bóc cụm lõi sai |
| Đếm nguyên cụm câu hỏi | "cpu hàng tray là gì" 12 lần vs lõi 38 lần |
| Cửa sổ kết bài 200 từ | Không chạm tới kết luận thật (CTA chiếm 200 từ cuối) |
| Retry 8s/16s khi hết hạn mức ngày | Đốt thêm lượt vô ích |

**Phát hiện vận hành quan trọng:** Gemini free giới hạn **20 lượt/ngày cho MỖI model**.
Hạn mức tính riêng từng model nên xoay vòng 5 model được ~100 lượt/ngày.

---

## Cập nhật trước đó — Công cụ viết bài bằng AI (2026-08-19)

Thêm tab thứ ba: dán từ khóa → AI viết bài → copy dán thẳng vào WordPress.

**File đã tạo:** package `writer/` (9 file), `gui/tab_writer.py`, `.env.example`, `prompts/giaphongpc.md`

**Ba quyết định thiết kế:**
- **Đổi nhà cung cấp AI bằng một dòng trong `.env`** — bắt đầu bằng Gemini miễn phí không cần
  thẻ tín dụng, chuyển sang Claude sau này không phải sửa code. Thư viện `anthropic` chỉ nạp
  khi thực sự dùng nên người xài Gemini không cần cài.
- **Prompt là của người dùng** — `writer/` chỉ thay `{keyword}` và nối ghi chú vào cuối,
  không hiểu và không sửa nội dung prompt. Thả file `.md` vào `prompts/` là giao diện tự thấy.
- **Clipboard giữ định dạng** — gọi Windows API qua ctypes ghi định dạng "HTML Format",
  để Ctrl+V vào WordPress ăn đúng thẻ H2 như khi copy từ ChatGPT.

**Kiểm chứng:** chạy thật trên gói Gemini miễn phí — bài 1.498 từ trong 55 giây, HTML sạch
(1 H1, 6 H2, 7 H3, 21 đoạn, 14 danh sách), 3 chỗ `[CẦN BỔ SUNG]` cho người dùng điền số liệu thật.

**Bốn lỗi đã phát hiện khi chạy thật** — chi tiết trong [`report/report-19-8-2026.md`](report/report-19-8-2026.md):
hộp thoại lỗi cắt còn 1 dòng; vứt bỏ thông điệp Google chỉ tên model thay thế;
`gemini-2.5-flash` ngừng mở cho người dùng mới; gói free hay trả 503 mà chưa có retry.

---

## Cập nhật trước đó — Giao diện đồ họa (2026-08-19)

Thêm ứng dụng cửa sổ Windows để dùng cả hai công cụ mà không cần gõ lệnh hay sửa `config.py`.

**File đã tạo:** package `gui/` (8 file), `seo_gui.pyw`, `Chay_giao_dien.bat`

**Đã làm:**
- Cửa sổ 2 tab, dùng tkinter có sẵn trong Python — **không cần cài thêm thư viện nào**
- Nhập từ khóa trực tiếp vào ô, mỗi dòng một từ
- Ô hiển thị tiến trình theo thời gian thực, tô màu cảnh báo và lỗi
- Bảng kết quả có ô lọc nhanh trên mọi cột
- Nút Dừng giữa chừng, **giữ lại toàn bộ kết quả đã thu được**
- Tab Suggest hiện ước tính số lượt hỏi và thời gian dự kiến, cập nhật theo tùy chọn
- File `.bat` bấm đúp để chạy, có thông báo rõ ràng nếu không tìm thấy Python

**Thay đổi ở code cũ:** thêm tham số tùy chọn `nen_dung=None` vào `quet_breakout()` và
`thu_thap()` để hỗ trợ dừng giữa chừng. Mặc định `None` nên dòng lệnh cũ **không bị ảnh hưởng**
(đã chạy lại để xác nhận).

**Một lỗi thiết kế thật đã phát hiện khi test:**

Bản đầu tiên cho luồng nền gọi `widget.after()` để báo kết quả về giao diện. Test sập ngay:

```
RuntimeError: main thread is not in main loop
```

Tkinter không cho phép luồng nền đụng vào giao diện, kể cả qua `after()`. Đã sửa: luồng nền
chỉ cất kết quả vào chính nó, luồng chính định kỳ 120ms kiểm tra xem xong chưa. Nguyên tắc
này đã ghi vào `gui/worker.py` để không ai lặp lại.

**Kiểm chứng:** chạy thật qua giao diện ra 8 dòng và xuất file thành công; bấm Dừng giữa
chừng dừng sau 1,5 giây và giữ nguyên 88 keyword đã thu; nút Chạy bật lại đúng trạng thái.

---

## Cập nhật trước đó — Khởi tạo dự án (2026-08-19)

Dựng từ số 0 hai công cụ thu thập từ khóa SEO, tách module, chạy kiểm chứng thật và đưa lên GitHub.

**File đã tạo:** 23 file code (xem cấu trúc trong `SEO_AI_WORKFLOW_GUIDE.md`)

**Đã làm:**
- Viết `trends_scrapper.py` — dò từ khóa Breakout (>5000%) qua Google Trends, chia lô 5 từ, retry lũy tiến chống chặn IP
- Viết `suggest_scrapper.py` — khai thác Google Suggest, ghép từ mồi + bảng chữ cái, tự phân loại ý định tìm kiếm
- Tách cả hai từ file đơn thành package (`trends/`, `suggest/`), mỗi file một nhiệm vụ
- Bỏ biến global, thay bằng đối tượng `Settings` truyền tường minh
- Thay dict trạng thái bằng class `TrendsFetcher` / `SuggestClient`
- Khởi tạo git, đẩy lên GitHub

**Ba lỗi thật đã phát hiện khi chạy và đã sửa:**

| Lỗi | Nguyên nhân | Cách xử lý |
|---|---|---|
| `TypeError: Retry.__init__() got an unexpected keyword argument 'method_whitelist'` | pytrends 4.9.2 không tương thích urllib3 2.x | Bỏ `retries=`/`backoff_factor=` khỏi `TrendReq()`, dùng retry tự viết |
| `UnicodeEncodeError: 'charmap' codec can't encode` | Console Windows dùng cp1252, vỡ log tiếng Việt | Ép `sys.stdout.reconfigure(encoding="utf-8")` |
| Rác `máy tính casio` trong kết quả (~1,3%) | Tiếng Việt: "máy tính" = computer VÀ calculator | Thêm bộ lọc vào `TU_KHOA_LOAI_BO` |

**Kiểm chứng:** Cả hai công cụ đã chạy đầy đủ trên máy thật, xuất file Excel đọc lại được bằng pandas, đúng số cột và số dòng.

Nhật ký chi tiết: [`docs/ai-journal/2026-08-19_khoi-tao-bo-cong-cu.md`](docs/ai-journal/2026-08-19_khoi-tao-bo-cong-cu.md)

---

## Vấn đề đang tồn tại (chưa chặn tiến độ)

| # | Vấn đề | Mức độ | Ghi chú |
|---|---|---|---|
| 1 | Google Suggest không cho biết lượng tìm kiếm/tháng | Trung bình | Giới hạn của nguồn miễn phí. Bù bằng Google Search Console sau 1–2 tháng |
| 2 | Nhóm "Thông tin sản phẩm" chiếm 45% (3.171 từ) | Thấp | Là nhóm gom chung, cần luật phân loại chi tiết hơn |
| 3 | `mua bán sửa chữa laptop quận bình thạnh` xếp nhầm vào "Khắc phục lỗi" | Thấp | Luật "sửa" chạy trước luật thương mại. Đảo thứ tự trong `LUAT_PHAN_LOAI` là xong |
| 4 | File Excel ngày 2026-08-19 còn ~90 dòng rác casio | Thấp | Bộ lọc đã thêm sau khi file được tạo. Chạy lại sẽ sạch |
| 5 | Google Trends chặn IP nếu chạy nhiều lần liên tiếp | Trung bình | Đã gặp thật: 1 lô bị bỏ qua lúc 15:07. Nên giãn cách ít nhất 1–2 giờ giữa các lần chạy |
| 6 | `gpt-5-mini` viết ngắn: ~2.100 từ so với chuẩn 3.000 | Trung bình | Không phải lỗi code. Cách gỡ: đổi sang `gpt-5`, hoặc dùng ô "Yêu cầu bổ sung" đòi viết dài hơn, hoặc hạ chuẩn trong `writer/config.py` |
| 7 | Cụm lõi từ khóa bóc chưa đủ ngắn với từ khóa dài | Trung bình | `lay_tu_khoa_loi()` cắt "cách kiểm tra ram máy tính có bị lỗi không" xuống còn 6 chữ "kiểm tra ram máy tính có bị lỗi". Đòi lặp 15–20 lần một mệnh đề 6 chữ là bất khả thi. Đo trên bài thật: cụm đó 7 lần (0,34%) nhưng "kiểm tra ram" tới 14 lần (0,68%) và có mặt ở 2 thẻ H2. Cần chốt lại cách bóc lõi — xem ghi chú bên dưới |
| 8 | AI đếm ký tự SEO Title sai | Thấp | Tự khai 55, thật 65. Bản chất mô hình ngôn ngữ, không sửa bằng prompt được. Bộ kiểm tra đã bắt được, sửa tay trước khi đăng |

---

## Lịch sử cập nhật

### 2026-08-19 — Khởi tạo dự án
Xem mục "Cập nhật mới nhất" ở trên.

<!--
HƯỚNG DẪN CHO PHIÊN AI SAU:
Khi có thay đổi mới, CHÈN mục mới ngay dưới dòng "## Cập nhật mới nhất",
đổi tiêu đề mục cũ thành "## Cập nhật trước đó — <tên> (<ngày>)",
và thêm một dòng tóm tắt vào phần "Lịch sử cập nhật" này.
Luôn cập nhật dòng "Cập nhật lần cuối" ở đầu file.
-->
