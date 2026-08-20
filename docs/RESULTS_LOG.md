# Nhật ký kết quả chạy

> Mỗi lần chạy công cụ ghi một dòng vào đây. Đây là chỗ theo dõi **hiệu quả** —
> lần chạy này có tốt hơn lần trước không, cấu hình nào cho kết quả tốt nhất.
>
> **Cách ghi:** thêm dòng mới vào ĐẦU bảng (mới nhất lên trên).

---

## Công cụ 1 — `trends_scrapper.py` (Google Trends)

| Ngày giờ | Tham số | Số seed | Breakout thu được | Thời gian | Ghi chú |
|---|---|---:|---:|---:|---|
| 2026-08-19 15:07 | mặc định | 20 | **4** | 418 giây | ⚠️ 1 lô bị Google chặn, bỏ qua 5 seed. Do chạy nhiều lần liên tiếp |
| 2026-08-19 14:48 | mặc định | 20 | **7** | 53 giây | ✅ Lần chạy sạch đầu tiên |

### Từ khóa Breakout đáng chú ý đã tìm được

| Từ khóa | Tăng trưởng | Đánh giá |
|---|---:|---|
| `dàn pc gaming` | 87.100% | ✅ Nên làm nội dung |
| `laptop gaming mỏng nhẹ` | 81.000% | ✅ Nên làm nội dung |
| `full bộ pc gaming giá rẻ` | 72.650% | ✅ Nên làm nội dung |
| `pc gaming cần thơ` | 60.950% | ⚠️ Tín hiệu địa phương — bỏ qua nếu chỉ bán ở TP.HCM |
| `ttg`, `ttgshop`, `phongvu` | 10.000–43.850% | ❌ Tên đối thủ — theo dõi, không làm từ khóa mục tiêu |

**Bài học:** Google Trends hay trả về tên thương hiệu đối thủ. Đây là bản chất công cụ,
không phải lỗi. Cần lọc bằng mắt trước khi đưa vào kế hoạch nội dung.

---

## Công cụ 2 — `suggest_scrapper.py` (Google Suggest)

| Ngày giờ | Tham số | Số seed | Keyword thu được | Thời gian | Ghi chú |
|---|---|---:|---:|---:|---|
| 2026-08-19 15:30 | mặc định (đầy đủ) | 24 | **7.045** | 13,3 phút | ✅ Lần chạy đầy đủ đầu tiên. Còn ~90 dòng rác casio |
| 2026-08-19 15:17 | `--quick` | 2 | 75 | 0,5 phút | Chạy thử kiểm chứng |

### Phân bổ theo nhóm ý định (lần chạy 15:30)

| Nhóm | Số lượng | Tỷ lệ | Ưu tiên |
|---|---:|---:|---|
| Khắc phục lỗi | 610 | 8,7% | ★★★ Làm trước — dễ lên top nhất |
| Khái niệm | 197 | 2,8% | ★★★ Xây uy tín |
| Hướng dẫn | 274 | 3,9% | ★★★ Kéo traffic đều |
| So sánh - Tư vấn | 1.699 | 24,1% | ★★ Chèn link sản phẩm |
| Thương mại | 1.094 | 15,5% | ★ Làm trang bán hàng, không viết blog |
| Thông tin sản phẩm | 3.171 | 45,0% | Nhóm gom chung, cần lọc thêm |

**Kết luận:** 1.081 keyword của 3 nhóm đầu đủ làm kế hoạch nội dung hơn 2 năm nếu đăng 1 bài/ngày.

**Bài học:** Nhóm "Thông tin sản phẩm" chiếm 45% là quá lớn — đây là nhóm mặc định khi không
khớp luật nào. Cần bổ sung luật phân loại chi tiết hơn trong `suggest/config.py`.

---

## Công cụ 3 — Tab "Viết bài" (Gemini / Claude)

| Ngày giờ | Từ khóa | Model | Số từ | Thời gian | Chi phí |
|---|---|---|---:|---:|---|
| 2026-08-20 10:07 | cách kiểm tra ram máy tính có bị lỗi không | **gpt-5** | 2.460 | 125 giây | 3.362 vào / 8.474 ra |
| 2026-08-20 09:57 | cách kiểm tra ram máy tính có bị lỗi không | **gpt-5-mini** | 2.061 | 79 giây | 3.362 vào / 7.149 ra |
| 2026-08-20 09:54 | cách kiểm tra ram máy tính có bị lỗi không | **gpt-5-mini** | 2.387 | 72 giây | 2.911 vào / 6.881 ra |
| 2026-08-19 17:43 | cách khắc phục loa máy tính bàn không nghe được | gemini-3.6-flash | 1.455 | ~55 giây | miễn phí |
| 2026-08-19 17:30 | cách kiểm tra ram máy tính có bị lỗi không | gemini-3.6-flash | 1.498 | 55 giây | miễn phí |

### Lần chạy thật đầu tiên bằng OpenAI gpt-5-mini (2026-08-20)

Kết quả chấm bằng `writer/auditor.py` trên chính hai bài ở bảng trên:

| Tiêu chí | Bài 09:54 (prompt cũ) | Bài 09:57 (prompt đã sửa) |
|---|---|---|
| Tổng số mục chưa đạt | 8 / 25 | **5 / 25** |
| Thẻ H2 | **0** ❌ | **11** ✅ |
| Số câu FAQ | **0** ❌ | **5** ✅ |
| External link | 2 ✅ | 1 ✅ |
| Từ khóa trong kết bài | có ✅ | có ✅ |
| Tổng số từ | 2.387 ❌ | 2.061 ❌ |
| SEO Title | 65 ký tự ❌ | 69 ký tự ❌ |

**Phát hiện lớn nhất:** gpt-5-mini **không tự viết `##`**. Nó viết tên mục thành dòng chữ
trơn ("Cần chuẩn bị gì", "Trả lời nhanh"), nên bài ra HTML **không có thẻ H2 nào** — vô giá
trị về SEO dù đọc vẫn xuôi. Gemini tự suy ra được cú pháp Markdown, gpt-5-mini thì không.
Đã thêm bảng cú pháp heading + khung bài mẫu vào `prompts/giaphongpc-tong-quat.md`; chạy lại
ra 11 H2 và 5 FAQ. FAQ về 0 chỉ là hệ quả kéo theo: `_dem_faq()` tìm dòng `## ...FAQ...`,
không có `##` thì không thấy khu vực FAQ.

**Bài học:** prompt viết cho model này chưa chắc chạy được với model kia. Đổi nhà cung cấp
là phải chạy lại một bài rồi soi bằng bộ kiểm tra, không được tin là "chắc cũng vậy".

**Còn tồn:** gpt-5-mini viết ngắn (~2.100 từ so với chuẩn 3.000) và đếm ký tự title sai
(tự khai 55, thật 65). Xem mục "Vấn đề đang tồn tại" trong `PROJECT_STATE.md`.

### gpt-5-mini và gpt-5 — so trực tiếp (2026-08-20)

Cùng từ khóa, cùng prompt, chấm lại cả hai bằng **thước đo mới** (cụm lõi + mật độ đã nới):

| | gpt-5-mini | gpt-5 |
|---|---|---|
| Điểm | **21 đạt / 4 chưa đạt** | 19 đạt / 6 chưa đạt |
| Số từ | 2.061 | 2.460 |
| Thời gian | 79 giây | 125 giây |
| Token ra | 7.149 | 8.474 |
| Chưa đạt | số từ · số lần từ khóa · từ khóa trong H2 · độ dài title | số từ · số lần từ khóa · độ dài title · **thừa external link** · **thiếu author bio** · **1 số liệu nghi bịa** |

**Kết luận:** `gpt-5` **không đáng tiền** cho việc này. Nó chấm thấp hơn, chậm gần gấp đôi,
đắt hơn nhiều lần mỗi bài, và những mục nó trượt lại nặng hơn — thiếu hẳn khối author bio
và bịa một số liệu, trong khi mini chỉ trượt mấy mục hình thức (dài title, số lần từ khóa).

⚠️ **Cảnh báo về độ tin cậy:** mỗi model mới chạy **một bài**. Kết quả này đủ để nói
"không có lý do gì phải đổi sang gpt-5", chưa đủ để nói "mini tốt hơn gpt-5". Muốn chắc thì
chạy thêm 3–5 từ khóa khác nhau.

**Cả hai đều không đạt 3.000 từ.** Đây là điểm chung, nên nhiều khả năng do prompt chưa ép
đủ mạnh về độ dài chứ không phải do model.

⚠️ Bảng `BANG_GIA` trong `writer/config.py` **chưa có dòng nào cho OpenAI**, nên ô chi phí
chỉ hiện số token thay vì tiền. Điền đơn giá lấy từ trang billing của OpenAI vào đó nếu
muốn thấy số tiền.

### ⚠ HẠN MỨC GÓI MIỄN PHÍ — điều quan trọng nhất cần biết

**~20 lượt/NGÀY cho MỖI model.** Không phải theo phút.

Google trả về `quotaId: GenerateRequestsPerDayPerProjectPerModel-FreeTier`, `quotaValue: 20`.
Chờ trong hôm nay không dùng được nữa; hạn mức thường được cấp lại khoảng **14–15 giờ VN**.

**Cách gỡ nhanh nhất: đổi model.** Hạn mức tính riêng cho từng model, nên hết model này
vẫn còn nguyên hạn mức ở model khác. Đã kiểm chứng ngày 2026-08-19: `gemini-3.6-flash`
hết 20 lượt trong khi 4 model khác vẫn dùng được bình thường.

Thứ tự ưu tiên đổi: `gemini-3.7-flash` → `gemini-3.6-flash` → `gemini-3.5-flash`
→ `gemini-flash-latest` → `gemini-3.1-flash-lite`

Nghĩa là mỗi ngày có khoảng **100 lượt miễn phí** nếu xoay vòng 5 model.

### Ghi chú quan trọng về model Gemini

| Model | Trạng thái |
|---|---|
| `gemini-2.5-flash` | ❌ Không còn mở cho người dùng mới (Google trả 404) |
| `gemini-3.6-flash` | ✅ **Đang dùng** — Google đề xuất thay thế cho 2.5 |
| `gemini-3.7-flash` | ⚠️ Có tồn tại nhưng hay quá tải (503) |

⚠️ Danh sách model từ `ListModels` **không đáng tin hoàn toàn** — `gemini-2.5-flash` vẫn nằm
trong danh sách nhưng gọi thì báo 404. Luôn tin thông điệp lỗi trực tiếp của Google hơn.

⚠️ Gói miễn phí hay trả **503 "high demand"**. Công cụ đã tự thử lại 3 lần (8s → 16s → 24s).
Nếu vẫn hỏng thì chờ vài phút, không phải lỗi cấu hình.

### So sánh chi phí nếu chuyển sang Claude

| Model | Chi phí/bài | 100 bài/tháng |
|---|---:|---:|
| Gemini (gói free) | 0đ | **0đ** |
| Claude Opus 5 | ~2.800đ | ~280.000đ |
| Claude Sonnet 5 | ~1.700đ | ~170.000đ |

---

## Chỉ số cần theo dõi về sau

Những số này chỉ đo được sau khi đã đăng bài, cần Google Search Console:

| Chỉ số | Đo ở đâu | Mục tiêu |
|---|---|---|
| Số bài đã đăng từ danh sách keyword | Tự đếm | — |
| Số keyword đã lên top 10 | Google Search Console | Tăng đều |
| Lượt hiển thị / lượt nhấp | Google Search Console | Tăng đều |
| Nhóm ý định nào ra traffic tốt nhất | Đối chiếu GSC với `Nhóm ý định` | Xác nhận thứ tự ưu tiên có đúng không |

> ⚠️ Google Suggest **không** cung cấp lượng tìm kiếm/tháng. Đây là giới hạn của nguồn miễn phí.
> Cách bù duy nhất là đăng bài rồi đo bằng Google Search Console sau 1–2 tháng.
