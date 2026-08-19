# Giao diện đồ họa cho hai công cụ

**Ngày:** 2026-08-19
**Giai đoạn:** 1b — Giao diện
**Trạng thái:** ✅ HOÀN THÀNH — đã test chạy thật và test nút Dừng

---

## Bối cảnh

Người dùng không biết lập trình. Để chạy công cụ phải gõ lệnh dài với đường dẫn Python đầy đủ,
và muốn đổi từ khóa thì phải mở `config.py` sửa code. Cả hai đều là rào cản thật.

Yêu cầu: giao diện để nhập từ khóa và xem kết quả.

**Lưu ý:** "giao diện web" từng nằm ở mục *đã quyết định không làm* trong `implementation_plan.md`.
Người dùng yêu cầu lại nên đảo quyết định, và đã ghi rõ lý do đảo vào file đó.

---

## Lựa chọn kỹ thuật

| Phương án | Ưu | Nhược | Chọn |
|---|---|---|---|
| **tkinter** | Có sẵn trong Python, không cài thêm gì, bấm đúp `.bat` là chạy | Giao diện hơi cũ | ✅ |
| Streamlit | Đẹp, bảng lọc tốt | Cài thêm ~50MB, vẫn phải gõ lệnh khởi động | ❌ |

Chọn tkinter vì người dùng đã vấp đúng vấn đề "Python không có trong PATH" — càng ít bước
cài đặt càng tốt.

---

## Đã làm

### Package `gui/` — 8 file, mỗi file một việc

| File | Nhiệm vụ |
|---|---|
| `app.py` | Cửa sổ chính, ghép hai tab |
| `tab_base.py` | Khung chung: nhập từ khóa, nút chạy/dừng, ô log, bảng kết quả |
| `tab_trends.py` | Tab Trends — chỉ khai báo tùy chọn riêng |
| `tab_suggest.py` | Tab Suggest — chỉ khai báo tùy chọn riêng |
| `widgets.py` | Ô log tô màu, bảng có lọc, ô nhập từ khóa |
| `worker.py` | Luồng nền + cờ dừng |
| `log_bridge.py` | Đưa log lên giao diện qua hàng đợi |

Hai tab giống nhau tới 80% nên phần chung gom hết vào `tab_base.py`. Tab con chỉ cài đặt
3 hàm: `tao_bang_tuy_chon()`, `tao_ham_thu_thap()`, `xuat_file()`.

**Nguyên tắc quan trọng:** `gui/` KHÔNG chứa logic thu thập. Nó chỉ gọi lại đúng các hàm
trong `trends/` và `suggest/`. Sửa cách thu thập thì sửa ở hai package đó, giao diện tự chạy theo.

### Thêm khả năng dừng giữa chừng

Thêm tham số tùy chọn `nen_dung=None` vào `quet_breakout()` và `thu_thap()`:

- `trends/scanner.py`: kiểm tra giữa các lô
- `suggest/collector.py`: kiểm tra giữa các seed **và** giữa các biến thể
  (mỗi seed mất ~30 giây, chờ hết seed mới dừng là quá lâu)

Khi dừng, **kết quả đã thu được vẫn giữ nguyên** và vẫn xuất ra file.

Mặc định `None` nên dòng lệnh cũ không bị ảnh hưởng — đã chạy lại để xác nhận.

### File `.bat` bấm đúp

`Chay_giao_dien.bat` gọi `pythonw.exe` (không hiện cửa sổ đen). Nếu không tìm thấy Python
ở đường dẫn mặc định thì thử `py` launcher, vẫn không có thì in hướng dẫn cài đặt rõ ràng
thay vì nháy tắt.

---

## Lỗi thiết kế thật đã phát hiện

### Luồng nền gọi `widget.after()` → sập

Bản đầu tiên cho luồng nền báo kết quả về giao diện bằng `self.after(0, callback)`.
Test sập ngay:

```
RuntimeError: main thread is not in main loop
```

**Nguyên nhân:** tkinter không cho phép luồng khác đụng vào giao diện, kể cả qua `after()`.
Đây là hiểu nhầm phổ biến — nhiều hướng dẫn trên mạng nói `after()` là thread-safe, thực tế không.

**Cách tìm ra:** viết test dựng cửa sổ rồi chạy thật một lượt thu thập nhỏ. Nếu chỉ test
"dựng widget có lỗi không" thì sẽ không bao giờ thấy lỗi này.

**Xử lý:** bỏ hoàn toàn callback chéo luồng.
- Luồng nền chỉ cất kết quả vào chính nó (`self.ket_qua`, `self.loi`)
- Luồng chính đã có sẵn vòng lặp 120ms để đọc log, giờ kiểm tra luôn xem luồng xong chưa

Cách này còn gọn hơn bản đầu vì tận dụng vòng lặp có sẵn.

---

## Kiểm chứng

| Kiểm tra | Kết quả |
|---|---|
| Dựng toàn bộ cây widget | ✅ Cửa sổ, 2 tab, ô nhập có sẵn 24 và 20 từ gốc |
| Ước tính thời gian tab Suggest | ✅ "≈ 1,080 lượt hỏi Google · dự kiến 11 phút" |
| Settings sinh đúng từ tùy chọn | ✅ geo/timeframe/rising/format đều khớp |
| Bảng kết quả + ô lọc nhanh | ✅ 2 dòng → lọc "cpu" → 1 dòng |
| **Chạy thật qua giao diện** | ✅ 8 dòng, xuất file Excel thành công |
| **Nút Dừng giữa chừng** | ✅ Dừng sau 1,5 giây, giữ nguyên 88 keyword đã thu |
| Nút Chạy bật lại sau khi dừng | ✅ normal / disabled đúng trạng thái |
| Dòng lệnh cũ không bị hỏng | ✅ `suggest_scrapper.py --quick` vẫn ra 11 keyword |

---

## Bài học cho phiên sau

1. **Test dựng widget là chưa đủ.** Phải chạy một lượt thu thập thật qua giao diện mới
   lộ ra lỗi đa luồng.
2. **Đừng tin `after()` là thread-safe.** Quy tắc an toàn: luồng nền chỉ ghi vào biến
   của chính nó, luồng chính chủ động đi lấy.
3. **Thêm tham số mới phải để mặc định `None`** để không phá code đang chạy. Đã xác nhận
   bằng cách chạy lại dòng lệnh cũ.

---

## Việc tiếp theo

Xem [`../../implementation_plan.md`](../../implementation_plan.md) — Giai đoạn 2:
chia nhỏ nhóm "Thông tin sản phẩm" và sửa lỗi xếp nhầm nhóm dịch vụ.
