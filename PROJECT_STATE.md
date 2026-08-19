# SEO Automation — Project State

> **Cập nhật lần cuối:** 2026-08-19 (Khởi tạo dự án + 2 công cụ hoàn chỉnh)
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

## Cập nhật mới nhất — Khởi tạo dự án (2026-08-19)

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
