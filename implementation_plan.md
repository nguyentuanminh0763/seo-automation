# Lộ trình triển khai

> Cập nhật lần cuối: 2026-08-19
>
> **Cách dùng:** đánh dấu `[x]` khi xong, kèm ngày. Việc bỏ thì ghi rõ lý do, đừng xóa —
> để phiên sau không đề xuất lại.

---

## Giai đoạn 1 — Thu thập từ khóa ✅ HOÀN THÀNH (2026-08-19)

- [x] Công cụ Google Trends bắt từ khóa Breakout — *2026-08-19*
- [x] Công cụ Google Suggest lấy từ khóa làm nội dung — *2026-08-19*
- [x] Tách module, mỗi file một nhiệm vụ — *2026-08-19*
- [x] Chạy kiểm chứng thật cả hai công cụ — *2026-08-19*
- [x] Đưa lên GitHub — *2026-08-19*
- [x] Dựng hệ thống tài liệu theo dõi tiến độ — *2026-08-19*

---

## Giai đoạn 2 — Làm sạch và nâng chất lượng dữ liệu 🔜 TIẾP THEO

Ưu tiên cao, làm được ngay, không cần công cụ mới.

- [ ] **Chia nhỏ nhóm "Thông tin sản phẩm"** (đang chiếm 45% — quá lớn)
      → Thêm luật vào `LUAT_PHAN_LOAI` trong `suggest/config.py`
      → Gợi ý tách: theo thương hiệu, theo thông số kỹ thuật, theo dòng sản phẩm
- [ ] **Sửa lỗi xếp nhầm nhóm dịch vụ**
      `mua bán sửa chữa laptop quận bình thạnh` đang bị xếp vào "Khắc phục lỗi"
      → Đảo khối `Thương mại` lên trên khối `Khắc phục lỗi` trong `LUAT_PHAN_LOAI`
- [ ] **Chạy lại `suggest_scrapper.py`** sau khi sửa xong hai việc trên, để có file sạch
- [ ] **Thêm cột "Địa phương"** đánh dấu từ khóa gắn tỉnh thành khác TP.HCM, để lọc nhanh

---

## Giai đoạn 3 — Theo dõi hiệu quả 📋 CHỜ

Chỉ làm được sau khi đã đăng bài một thời gian.

- [ ] Kết nối Google Search Console để biết lượng tìm kiếm thật
      → Đây là cách **duy nhất** bù cho việc Google Suggest không cho biết search volume
- [ ] Đối chiếu: nhóm ý định nào thực sự ra traffic, có đúng thứ tự ưu tiên đang giả định không
- [ ] Ghi kết quả vào `docs/RESULTS_LOG.md` phần "Chỉ số cần theo dõi về sau"

---

## Giai đoạn 4 — Mở rộng công cụ 💡 Ý TƯỞNG

Chưa cam kết. Cân nhắc khi giai đoạn 2 và 3 đã ổn.

- [ ] **People Also Ask** — lấy phần "Mọi người cũng hỏi" của Google
      ⚠️ Rủi ro: dễ bị chặn IP hơn Suggest nhiều, cần cân nhắc kỹ
- [ ] **Theo dõi thứ hạng từ khóa** — kiểm tra vị trí của giaphongpc.vn theo thời gian
- [ ] **So sánh giữa các lần chạy** — công cụ đọc 2 file Excel, chỉ ra từ khóa mới xuất hiện
- [ ] **Tự động chạy hàng tuần** — Task Scheduler của Windows chạy `trends_scrapper.py`
- [ ] **Gộp kết quả nhiều lần chạy** — hiện mỗi lần tạo file riêng, chưa có bản tổng hợp

---

## Đã cân nhắc và quyết định KHÔNG làm

| Việc | Lý do bỏ |
|---|---|
| Chuyển sang database (SQLite/Postgres) | Người dùng làm SEO, không phải lập trình viên. Excel là định dạng họ dùng hàng ngày |
| Giao diện web | Quá mức cần thiết cho công cụ chạy hàng tuần. Dòng lệnh là đủ |
| Dùng API trả phí (Ahrefs, Semrush) | Chi phí cao. Nguồn miễn phí đã cho 7.045 keyword, đủ dùng nhiều năm |
| Gộp hai công cụ làm một | Chúng trả lời hai câu hỏi khác nhau, tần suất chạy khác nhau. Tách riêng dễ hiểu hơn |
| Dùng lớp retry sẵn của pytrends | Không tương thích urllib3 2.x. Retry tự viết kiểm soát tốt hơn |
