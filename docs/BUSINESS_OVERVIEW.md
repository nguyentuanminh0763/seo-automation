# Bối cảnh kinh doanh — giaphongpc.vn

> Bối cảnh này quyết định từ khóa nào đáng theo đuổi và nội dung nào nên viết.
> Đọc trước khi sửa danh sách từ khóa gốc trong `trends/config.py` hoặc `suggest/config.py`.

---

## Doanh nghiệp

**Gia Phong PC** — bán lẻ máy tính và linh kiện công nghệ, thị trường chính **TP.HCM**.

## Nhóm sản phẩm và dịch vụ

| Nhóm | Chi tiết |
|---|---|
| **Máy tính bộ lắp ráp** | PC Gaming, PC Đồ Họa, PC Giả Lập, PC AI, máy tính bộ cũ |
| **Laptop** | Laptop Gaming, Laptop Văn Phòng, Laptop cũ, Laptop AI |
| **Linh kiện mới và cũ** | CPU Intel/AMD, card RTX 5060 / RTX 5060 Ti, tản nhiệt, RAM, mainboard |
| **Màn hình** | Màn hình gaming, màn hình cong, màn hình phẳng 2K và FHD |
| **Gaming Gear** | Chuột, bàn phím cơ, tai nghe |
| **Dịch vụ** | Sửa máy tính, thu mua PC cũ giá cao tại TP.HCM |

---

## Ảnh hưởng tới chiến lược từ khóa

### Nên theo đuổi
- Từ khóa **hướng dẫn và sửa lỗi** — người gặp sự cố máy tính là khách hàng tiềm năng
  của cả dịch vụ sửa chữa lẫn linh kiện thay thế
- Từ khóa **so sánh linh kiện** — người đang phân vân chọn mua, dễ chốt đơn
- Từ khóa **giải thích thuật ngữ** (`cpu hàng tray là gì`) — xây uy tín chuyên môn
- Từ khóa gắn **TP.HCM** và các quận — đúng địa bàn phục vụ

### Nên bỏ qua
- Từ khóa gắn **tỉnh thành khác** (`pc gaming cần thơ`) nếu không giao hàng toàn quốc
- **Tên thương hiệu đối thủ** (`ttg`, `ttgshop`, `phongvu`) — theo dõi thị trường được,
  nhưng không làm từ khóa mục tiêu
- Từ khóa về **thiết bị ngoài ngành** — điện thoại, máy ảnh, tivi

### Bẫy ngôn ngữ cần lọc
Tiếng Việt dùng chung từ **"máy tính"** cho:
- **Computer** (đúng mảng kinh doanh) ✅
- **Máy tính cầm tay Casio** (hoàn toàn không liên quan) ❌

Không lọc thì kết quả lẫn đầy `sửa máy tính casio 570`, `máy tính fx-580`.
Đã đo thực tế: chiếm khoảng 1,3% kết quả thu về.
Bộ lọc nằm ở `TU_KHOA_LOAI_BO` trong [`../suggest/config.py`](../suggest/config.py).

---

## Cách dùng kết quả để làm nội dung

| Nhóm ý định | Người tìm đang ở đâu | Nên làm gì |
|---|---|---|
| Khắc phục lỗi | Đang gặp sự cố, cần giúp gấp | Bài hướng dẫn sửa lỗi, chèn CTA dịch vụ sửa chữa |
| Khái niệm | Đang tìm hiểu, chưa mua | Bài giải thích ngắn gọn, xây uy tín |
| Hướng dẫn | Muốn tự làm | Bài từng bước có ảnh, gợi ý linh kiện liên quan |
| So sánh - Tư vấn | Sắp mua, đang phân vân | Bài so sánh, chèn link sản phẩm đang bán |
| Thương mại | Sẵn sàng mua | **Trang danh mục sản phẩm**, không viết blog |
| Thông tin sản phẩm | Đa dạng | Trang sản phẩm hoặc danh mục |

**Nguyên tắc:** bốn nhóm đầu là nội dung kéo traffic. Nhóm Thương mại đừng viết blog —
người ta muốn mua, không muốn đọc.
