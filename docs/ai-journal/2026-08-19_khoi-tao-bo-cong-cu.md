# Khởi tạo bộ công cụ SEO

**Ngày:** 2026-08-19
**Giai đoạn:** 1 — Thu thập từ khóa
**Trạng thái:** ✅ HOÀN THÀNH — cả hai công cụ đã chạy thật, ra kết quả thật

---

## Mục tiêu phiên làm việc

Xây công cụ Python tự động tìm từ khóa đột biến trên Google Trends cho giaphongpc.vn.
Trong quá trình làm, phát sinh thêm nhu cầu lấy từ khóa dạng câu hỏi để viết bài,
nên bổ sung công cụ thứ hai dùng Google Suggest.

---

## Đã làm

### 1. Dựng môi trường
Máy chưa có Python. Cài Python 3.12.10 qua winget, cùng pytrends, pandas, openpyxl, requests.

**Phát hiện:** Python cài ở user scope nên **không nằm trong PATH**. Mọi lệnh phải gọi
đường dẫn tuyệt đối `C:\Users\PC\AppData\Local\Programs\Python\Python312\python.exe`.

### 2. Công cụ 1 — `trends_scrapper.py`
Dò từ khóa Breakout (tăng >5000%) qua Google Trends.

- Chia lô tối đa 5 từ khóa mỗi lần (giới hạn cứng của Google)
- Nghỉ ngẫu nhiên 5–12 giây giữa các lô
- Retry lũy tiến 60s → 120s → 180s, xoay proxy, đổi User-Agent
- Lọc theo nhãn `Breakout` hoặc giá trị số ≥ 5000

### 3. Công cụ 2 — `suggest_scrapper.py`
Khai thác Google Suggest lấy từ khóa dạng câu hỏi để làm nội dung.

- Ghép "từ mồi" (`cách`, `là gì`, `so sánh`...) vào trước/sau từ gốc
- Quét thêm bảng chữ cái a–z
- Mỗi từ gốc sinh 45 truy vấn, mỗi truy vấn trả tối đa 10 gợi ý
- Tự phân loại theo ý định tìm kiếm, xuất Excel nhiều sheet

### 4. Tách module
Ban đầu mỗi công cụ là một file lớn (~430 dòng). Người dùng yêu cầu tách cho dễ nhìn.

Kết quả: hai package `trends/` và `suggest/`, mỗi package 9 file, mỗi file một nhiệm vụ.
Hai cải tiến thật khi tách, không chỉ cắt file:
- Bỏ hoàn toàn biến global (`global TIMEFRAME, GEO`), thay bằng dataclass `Settings` truyền tường minh
- Thay dict trạng thái truyền qua lại bằng class `TrendsFetcher` / `SuggestClient` tự giữ trạng thái

### 5. Đưa lên GitHub
Repo public: https://github.com/nguyentuanminh0763/seo-automation
23 file code, `output/` bị chặn bởi `.gitignore`.

---

## Ba lỗi thật đã phát hiện

Điểm chung: **không lỗi nào phát hiện được bằng cách đọc code**. Cả ba chỉ lộ ra khi chạy thật.

### Lỗi 1 — pytrends không tương thích urllib3 2.x (nghiêm trọng)

```
TypeError: Retry.__init__() got an unexpected keyword argument 'method_whitelist'
```

**Nguyên nhân:** pytrends 4.9.2 gọi `urllib3.Retry(method_whitelist=...)`. Tham số này đã bị
urllib3 2.x xóa (đổi tên thành `allowed_methods`). Chỉ cần truyền `retries=` hoặc
`backoff_factor=` vào `TrendReq()` là mọi truy vấn hỏng.

**Cách tìm ra:** chạy test cô lập từng tham số của `TrendReq()` để khoanh vùng.

**Xử lý:** bỏ hai tham số đó. Vòng retry tự viết ở `trends/fetcher.py` mạnh hơn và kiểm soát tốt hơn.

### Lỗi 2 — Console Windows dùng cp1252

```
UnicodeEncodeError: 'charmap' codec can't encode character '\u1eae'
```

Log tiếng Việt có dấu làm vỡ toàn bộ output.

**Xử lý:** ép `sys.stdout.reconfigure(encoding="utf-8", errors="replace")` ngay đầu chương trình.

### Lỗi 3 — Bẫy ngôn ngữ "máy tính"

Kết quả lẫn `sửa máy tính casio 570`, `máy tính fx-580` — máy tính cầm tay, không phải PC.
Tiếng Việt dùng chung từ "máy tính" cho cả computer lẫn calculator.

**Đo được:** chiếm ~1,3% (khoảng 90/7.045 dòng).

**Xử lý:** thêm `casio`, `cầm tay`, `fx-570`... vào `TU_KHOA_LOAI_BO` trong `suggest/config.py`.
Đã test xác nhận lọc đúng dòng rác, giữ nguyên dòng tốt.

---

## Kiểm chứng

| Kiểm tra | Kết quả |
|---|---|
| `trends_scrapper.py` chạy đầy đủ | ✅ 7 từ khóa Breakout / 53 giây |
| `suggest_scrapper.py` chạy đầy đủ | ✅ 7.045 từ khóa / 13,3 phút |
| Đọc lại file Excel bằng pandas | ✅ Đúng số cột, đúng số dòng |
| Cơ chế chống chặn IP | ✅ Đã kiểm chứng thật — xem ghi chú dưới |
| Push GitHub, không lọt file `output/` | ✅ 23 file, không có `.xlsx` nào |

**Ghi chú về cơ chế chống chặn:** lần chạy lúc 15:07 bị Google chặn thật ở lô đầu tiên,
do đã gọi API liên tục suốt 20 phút trước đó. Script xử lý đúng như thiết kế: thử lại,
chờ 60s rồi 120s, vẫn hỏng thì ghi log cảnh báo và bỏ qua lô đó để chạy tiếp 3 lô còn lại.
Không sập, vẫn ra báo cáo. Coi như một lần diễn tập thật.

---

## Bài học cho phiên sau

1. **Luôn chạy thật trước khi báo hoàn thành.** Ba lỗi trên đều vô hình khi đọc code.
2. **Khoanh vùng lỗi bằng test cô lập.** Lỗi urllib3 chỉ tìm ra khi thử từng tham số riêng lẻ.
3. **Kiểm tra chất lượng dữ liệu đầu ra, không chỉ kiểm tra script chạy xong.**
   Rác casio chỉ lộ ra khi đọc kỹ file Excel.
4. **Giãn cách các lần chạy Google Trends ít nhất 1–2 giờ**, nếu không sẽ bị chặn IP.

---

## Việc tiếp theo

Xem [`../../implementation_plan.md`](../../implementation_plan.md) — Giai đoạn 2:
chia nhỏ nhóm "Thông tin sản phẩm" (đang chiếm 45%) và sửa lỗi xếp nhầm nhóm dịch vụ.
