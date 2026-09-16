# CLAUDE RULES — SEO AUTOMATION (giaphongpc.vn)

> Luật làm việc bền vững cho mọi phiên AI trên dự án này.
> Đọc file này TRƯỚC KHI thay đổi bất cứ thứ gì.

---

## Nguyên tắc cốt lõi

- **Không viết lại từ đầu.** Cả hai công cụ đã chạy thật và ra kết quả thật. Chỉ cải tiến từng phần.
- **Giữ kiến trúc package hiện tại.** Mỗi file làm đúng một việc. Không gộp ngược về một file lớn.
- **Không chuyển sang TypeScript.** Luật này còn nguyên, kể cả trong giao diện web
  (`web/` viết bằng JavaScript thuần).
- ~~**Không dùng framework nặng.**~~ **ĐÃ ĐẢO QUYẾT ĐỊNH 2026-09-16.** Người dùng yêu cầu
  giao diện web chuyên nghiệp hơn và tự chọn FastAPI sau khi được trình bày đánh đổi.
  Phạm vi của ngoại lệ này: **chỉ `webapi/` và `web/`**. Ba package lõi `trends/`,
  `suggest/`, `writer/` vẫn không được phép phụ thuộc vào framework nào — chúng phải
  chạy được bằng dòng lệnh mà không cần cài FastAPI.
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

### 4. Tkinter: luồng nền KHÔNG được đụng vào giao diện

Luồng nền tuyệt đối không gọi bất cứ hàm nào của tkinter, **kể cả `widget.after()`**.
Bản đầu tiên của giao diện làm vậy và sập ngay khi test:

```
RuntimeError: main thread is not in main loop
```

Cách đúng đã áp dụng: luồng nền chỉ cất kết quả vào chính nó (`gui/worker.py`),
luồng chính định kỳ 120ms kiểm tra xem xong chưa (`gui/tab_base.py`).
Log cũng đi qua hàng đợi chứ không ghi thẳng lên giao diện.

### 5. Giao diện web: mọi thứ chỉ nghe ở 127.0.0.1

`webapi/` đọc được file trên máy và chạy được công cụ thu thập. Ba chốt an toàn trong
`webapi/server.py` **không được gỡ**:

1. Chỉ nghe `127.0.0.1`. Đổi sang `0.0.0.0` là mở cửa cho cả mạng LAN.
2. Chỉ nhận yêu cầu có `Host` là localhost (chặn kiểu tấn công DNS rebinding).
3. Không bật CORS cho nguồn lạ — chỉ mở cổng 5173 khi chạy `python seo_web.py --dev`.

Đường dẫn tải file (`/api/tai-ve/`) phải luôn kiểm tra file nằm trong `output/`.
Bỏ chốt đó thì một tên file kiểu `../../.env` lôi được API key ra ngoài.

### 6. Hai công cụ thu thập KHÔNG được chạy song song

`webapi/jobs.py` cho Trends và Suggest dùng chung một khóa. Chạy song song = gấp đôi số
lần hỏi Google từ cùng một IP. Thêm màn Viết bài sau này thì nó phải có khóa **riêng**,
vì gọi OpenAI/Gemini chứ không gọi Google.

### 7. Git phải dùng remote HTTPS

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

## Luật về giao diện web

- Thư mục `web/dist/` **được commit** (cố ý). Người dùng không cài Node.js, nên bản build
  phải nằm sẵn trong repo để bấm đúp là chạy. Sửa `web/src/` xong **phải chạy lại
  `npm run build` rồi commit cả `web/dist/`**, không thì người dùng vẫn thấy bản cũ.
- Tên file build ép cố định `app.js` / `app.css` (khai trong `web/vite.config.js`).
  Không bật lại mã băm của Vite — mỗi lần sửa sẽ sinh tên file mới và làm rác lịch sử git.
- `webapi/` **không chứa logic thu thập**, giống hệt `gui/`. Nó chỉ gọi lại hàm trong
  `trends/` và `suggest/`.

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
