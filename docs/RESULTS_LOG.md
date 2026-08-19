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
| 2026-08-19 17:43 | cách khắc phục loa máy tính bàn không nghe được | gemini-3.6-flash | 1.455 | ~55 giây | miễn phí |
| 2026-08-19 17:30 | cách kiểm tra ram máy tính có bị lỗi không | gemini-3.6-flash | 1.498 | 55 giây | miễn phí |

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
