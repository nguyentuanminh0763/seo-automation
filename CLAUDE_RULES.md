# CLAUDE RULES — SEO AUTOMATION (giaphongpc.vn)

> Luật làm việc bền vững cho mọi phiên AI trên dự án này.
> Đọc file này TRƯỚC KHI thay đổi bất cứ thứ gì.

---

## Nguyên tắc cốt lõi

- **Không viết lại từ đầu.** Cả hai công cụ đã chạy thật và ra kết quả thật. Chỉ cải tiến từng phần.
- **Giữ kiến trúc package hiện tại.** Mỗi file làm đúng một việc. Không gộp ngược về một file lớn.
- **Không chuyển sang TypeScript, không dùng framework nặng.** Đây là script tự động hóa, không phải web app.
- **Không thêm database.** Kết quả xuất ra Excel/CSV là đủ. Người dùng làm SEO, không phải lập trình viên.
- **Mọi cấu hình phải nằm trong `config.py`.** Tuyệt đối không hardcode từ khóa, ngưỡng lọc, hay độ trễ vào code logic.

---

## Bối cảnh người dùng

- Người dùng **không biết lập trình**. Mọi giải thích phải bằng tiếng Việt, tránh thuật ngữ kỹ thuật.
- Khi hướng dẫn chạy lệnh, luôn đưa lệnh đầy đủ có thể copy-paste ngay.
- Khi sửa code, phải nói rõ **file nào, dòng nào, sửa để làm gì**.

---

## Luật kỹ thuật bắt buộc

### 1. Python không nằm trong PATH

Máy này cài Python 3.12.10 ở đường dẫn dưới nhưng **không có trong PATH**:

```
C:\Users\PC\AppData\Local\Programs\Python\Python312\python.exe
```

Luôn gọi bằng đường dẫn tuyệt đối. Dùng `python -m pip`, không dùng `pip` trực tiếp.

### 2. Console Windows dùng cp1252

Mọi script in tiếng Việt **bắt buộc** gọi dòng này trước khi log bất cứ thứ gì:

```python
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
```

Đã được xử lý sẵn trong `trends/logger.py` và `suggest/logger.py`. Không xóa.

### 3. pytrends không tương thích urllib3 2.x

**KHÔNG BAO GIỜ** truyền `retries=` hoặc `backoff_factor=` vào `TrendReq()`.
pytrends 4.9.2 gọi `urllib3.Retry(method_whitelist=...)` — tham số này đã bị urllib3 2.x xóa,
gây `TypeError` làm hỏng toàn bộ truy vấn. Vòng retry tự viết ở `trends/fetcher.py` đã thay thế.

### 4. Git phải dùng remote HTTPS

Khóa SSH trên máy thuộc tài khoản `khuongngocdoan`, không có quyền ghi vào repo của
`nguyentuanminh0763`. Push qua SSH luôn bị từ chối. Luôn dùng:

```
https://github.com/nguyentuanminh0763/seo-automation.git
```

---

## Luật chống chặn IP

Cả hai công cụ đều dùng API **không chính thức** của Google. Vi phạm các luật dưới đây sẽ bị chặn IP:

- Google Trends: tối đa **5 từ khóa mỗi lô** (giới hạn cứng), nghỉ **5–12 giây** giữa các lô.
- Google Suggest: nghỉ **0,3–0,9 giây** giữa các lượt hỏi.
- Không bao giờ bỏ `try-except` quanh lệnh gọi API. Một lô hỏng chỉ được bỏ qua, không được làm sập script.
- Không giảm độ trễ để chạy nhanh hơn. Chạy chậm mà xong còn hơn bị chặn IP vài giờ.

---

## Luật về dữ liệu

- **Thư mục `output/` KHÔNG BAO GIỜ được commit.** Repo đang để public; đó là kế hoạch nội dung
  của doanh nghiệp, đối thủ đọc được là mất lợi thế. Đã chặn trong `.gitignore`.
- Không đưa số liệu keyword cụ thể vào README hay tài liệu công khai, trừ vài ví dụ minh họa.

---

## Quy ước commit — BẮT BUỘC

Thông điệp commit phải viết bằng **tiếng Anh** và có **prefix chuẩn** (Conventional Commits).
Đây là ngoại lệ duy nhất so với luật "mọi thứ bằng tiếng Việt" — tài liệu và chú thích code
vẫn tiếng Việt, chỉ riêng commit dùng tiếng Anh.

| Prefix | Dùng khi |
|---|---|
| `feat:` | Thêm tính năng mới |
| `fix:` | Sửa lỗi |
| `docs:` | Chỉ thay đổi tài liệu |
| `refactor:` | Đổi cấu trúc code, không đổi hành vi |
| `chore:` | Việc lặt vặt: cấu hình, dependency, .gitignore |
| `perf:` | Cải thiện tốc độ |
| `test:` | Thêm hoặc sửa kiểm thử |

**Định dạng:**

```
<prefix>: <tóm tắt ngắn, chữ thường, không dấu chấm cuối>

<Phần thân giải thích LÝ DO thay đổi, không phải liệt kê lại code.
Xuống dòng ở khoảng 72 ký tự.>
```

Ví dụ đúng:

```
fix: drop retries kwarg from TrendReq for urllib3 2.x

pytrends 4.9.2 calls urllib3 Retry(method_whitelist=...), which was
removed in urllib3 2.x. Passing retries= broke every request.
```

Ví dụ sai: `Sửa lỗi pytrends`, `update code`, `fix bug`.

---

## Quy trình cho thay đổi lớn

Trước khi làm:
1. Đọc `PROJECT_STATE.md` để biết hiện trạng
2. Xác định file bị ảnh hưởng và mức rủi ro
3. Đề xuất kế hoạch nhỏ, chờ xác nhận nếu rủi ro trung bình trở lên

Sau khi làm:
1. **Chạy thật để kiểm chứng** — không báo hoàn thành khi chưa chạy
2. Cập nhật `PROJECT_STATE.md`
3. Ghi nhật ký vào `docs/ai-journal/`
4. Ghi kết quả đo được vào `docs/RESULTS_LOG.md` nếu có chạy công cụ

---

## Điều tuyệt đối tránh

- ❌ Báo "đã xong" khi chưa chạy thử thật
- ❌ Commit file trong `output/`
- ❌ Hardcode từ khóa vào file logic thay vì `config.py`
- ❌ Giảm độ trễ chống chặn để chạy nhanh
- ❌ Thêm phụ thuộc mới mà không cập nhật `requirements.txt`
