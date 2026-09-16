# 2026-09-16 — Chạy thật giao diện web, và cái lỗi chỉ trình duyệt thật mới bắt được

> Tiếp nối [`2026-09-16_giao-dien-web-react.md`](2026-09-16_giao-dien-web-react.md).
> Phiên đó chạy trên đám mây nên không đụng được máy người dùng; nó viết xong code và để
> lại đúng một việc: **gọi Google thật một lần**.

---

## Việc đã làm

1. Kéo nhánh `claude/optimistic-wright-if6kx2` về máy
2. Cài `fastapi` + `uvicorn` qua `requirements.txt`
3. Mở giao diện web, chạy thật Google Trends với đúng 5 từ khóa
4. Tìm ra và sửa một lỗi
5. Chạy thật lại để xác nhận bản vá

---

## Kết quả xác minh

**Cài đặt:** `fastapi 0.141.1`, `uvicorn 0.52.4`. Máy chủ lên ở `http://127.0.0.1:8765`,
giao diện mở được, điền sẵn 20 từ khóa mặc định đọc từ `trends/config.py`.

**Ba lượt chạy thật**, cùng 5 từ khóa `rtx 5060 ti · rtx 5060 · cpu hang tray ·
tan nhiet nuoc · ram ddr5`, 4,9–6 giây mỗi lượt, đều ra kết quả thật.
Số liệu đầy đủ trong [`../RESULTS_LOG.md`](../RESULTS_LOG.md).

**Điều nghi ngờ nhất hóa ra không sao.** Phiên trước lo `nen_dung` truyền xuống
`quet_breakout()` nay là hàm của lớp `Viec` thay vì `LuongChay`. Chạy đúng ngay lần đầu —
hợp đồng chỉ là "hàm không tham số trả về bool", cả hai lớp đều thỏa. Đọc code là đủ thấy,
nhưng luật dự án cấm kết luận kiểu đó, và đúng là chạy thật mới ra chuyện khác.

**Ba chốt an toàn cũng kiểm luôn, đều giữ được:** đường dẫn `..%2F..%2F.env` → 404,
`Host: evil.com` → 400, file xuất ra tải về được 5.153 byte và mở lại bằng pandas đủ 8 cột.

---

## Lỗi tìm được: nhật ký tự chép lại chính nó, mãi mãi

### Hiện tượng

Việc chạy xong khoảng 3 giây thì nhật ký hiện lại **toàn bộ** từ đầu, lần hai. Rồi lần ba.
Đếm bằng code trong trình duyệt:

| Thời điểm | Số bản sao của nhật ký |
|---|---:|
| ngay sau khi xong | 20 |
| 15 giây sau | 27 |

Không có điểm dừng. Mỗi lần lặp là một kết nối HTTP mới tới máy chủ — đo được **33 lần**
cho một lần chạy.

### Nguyên nhân gốc

Máy chủ gửi log ra trình duyệt bằng SSE (`GET /api/viec/{id}/dong`). Việc chạy xong thì hàm
sinh sự kiện `return` — kênh đóng lại **một cách bình thường**.

Nhưng `EventSource` của trình duyệt coi **mọi** lần dòng chảy kết thúc là rớt mạng, và tự
kết nối lại sau vài giây. Đó là hành vi mặc định, không tắt được.

Kết nối mới thì máy chủ làm đúng việc nó được viết ra để làm: **phát lại toàn bộ lịch sử**
(tính năng "tải lại trang giữa chừng vẫn thấy tiến trình", `webapi/jobs.py` → `dang_ky_nghe`).
Nên log bị cộng thêm một bản. Xong lại đóng kênh. Trình duyệt lại kết nối lại. Vòng lặp.

Hai tính năng đều đúng khi đứng riêng; ghép lại thành vòng lặp vô tận.

### Vì sao chốt chặn viết sẵn không cứu được

Phiên trước đã lường trước chuyện này và viết:

```js
nguon.onerror = () => {
  if (nguon.readyState === EventSource.CLOSED) khiCoSuKien({ loai: 'ket_thuc' })
}
```

Nhánh trong `if` **không bao giờ chạy**. Máy chủ đóng kênh bình thường thì `readyState`
chuyển sang `CONNECTING` (nghĩa là "đang kết nối lại"), không phải `CLOSED`. `CLOSED` chỉ
xuất hiện khi chính mình gọi `close()`, hoặc khi trình duyệt chịu thua hẳn.

Đây là bẫy đáng nhớ: **code phòng thủ trông có vẻ đúng, chạy không lỗi, mà vô tác dụng.**
Không có lỗi nào được ném ra để ai đó nhận ra.

### Cách sửa

Máy chủ vốn đã gửi sẵn một sự kiện `ket_thuc` khi xong. Nhận được thì tự đóng kênh —
một dòng trong `web/src/api.js`:

```js
if (suKien.loai === 'ket_thuc') nguon.close()
```

Không sửa gì ở máy chủ. Không thêm thư viện. Chốt `onerror` giữ nguyên làm chặn cuối cho
trường hợp máy chủ tắt giữa chừng, kèm chú thích nói rõ **vì sao không dùng nó để bắt lúc
việc xong** — để phiên sau không gỡ bản vá này ra rồi tin vào nó.

### Đo lại sau khi sửa

| | Trước | Sau |
|---|---:|---:|
| Số lần trình duyệt kết nối lại | 33 | **1** |
| Số bản sao nhật ký (sau 40 giây) | 27 và đang tăng | **1** |

---

## Bài học

**48 phép thử với dữ liệu giả không thể bắt được lỗi này**, và đó không phải do viết ẩu.
Chúng dựng phản hồi giả rồi cho đi qua hàm xử lý thật — cách làm đúng. Nhưng lỗi này không
nằm trong code của dự án: nó nằm ở **hành vi mặc định của trình duyệt sau khi máy chủ đóng
kết nối**. Muốn thấy phải có trình duyệt thật, và phải **chờ vài giây sau khi việc đã xong**
thay vì kiểm xong là đóng.

Đây là lỗi thứ 16 của dự án chỉ lộ ra khi chạy thật. Luật "không báo xong khi chưa chạy
thật" trong `CLAUDE_RULES.md` lại đúng thêm một lần.

Một chi tiết nữa đáng ghi: cùng 5 từ khóa, cùng khung thời gian, ba lượt chạy cách nhau
3 phút cho **ba kết quả khác nhau**. `related_queries()` của Google Trends vốn không ổn
định. Nghĩa là đừng kết luận gì từ một lần chạy duy nhất.

---

## Còn tồn

**Tải lại trang là mất kết quả đang xem** (mục 15 trong `PROJECT_STATE.md`). Kết quả vẫn
nằm nguyên trong bộ nhớ máy chủ, đọc được bằng `/api/viec`, nhưng giao diện không nhớ mã
việc nên không nối lại được. Phần phát lại lịch sử ở `webapi/jobs.py` đã viết sẵn mà chưa
ai dùng tới. Đáng làm vì Suggest chạy 13 phút — lỡ tay F5 là nhìn màn hình trống trong khi
máy chủ vẫn đang chạy ngon lành.

**Chưa chạy Suggest qua giao diện web.** Cố ý: 11 phút và hơn 1.000 lượt hỏi Google, mà nó
đi qua đúng đường dẫn mã như Trends.

---

## File đã sửa

```
web/src/api.js      — bản vá (1 dòng) + chú thích cảnh báo về onerror
web/dist/app.js     — build lại bằng npm run build
```
