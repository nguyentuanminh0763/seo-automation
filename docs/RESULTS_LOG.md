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
