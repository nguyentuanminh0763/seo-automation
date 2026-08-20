# 2026-08-20 — Vì sao tool viết bài "chậm hơn ChatGPT", và sửa thế nào

## Câu hỏi

Người dùng thấy viết bài bằng tool chậm hơn dán prompt vào ChatGPT, và muốn xem quy trình
gọi API có chỗ nào tối ưu được không. Kèm một yêu cầu quan trọng: **muốn chạy thử thì phải
hỏi**, để họ tự chạy cho đỡ tốn token.

Nghĩa là toàn bộ phiên này phải phân tích và kiểm chứng mà **không được gọi API thật**.

## Bước 1 — Đo trước khi đoán

Đo từng phần code cục bộ trên một bài đã lưu sẵn:

| Việc | Thời gian |
|---|---:|
| Ghép prompt | 0,0 ms |
| Markdown → HTML | 1,4 ms |
| Đếm từ | 0,5 ms |
| Chấm 25 tiêu chí SEO | 29,4 ms |
| **Tổng code cục bộ** | **31 ms** |

So với 94 giây một bài: code chiếm **0,03%**. Tối ưu code là vô nghĩa. Toàn bộ nằm ở cuộc
gọi OpenAI.

Đây là lý do phải đo trước: nếu lao vào tối ưu vòng lặp hay bộ đếm SEO thì mất cả buổi để
tiết kiệm 20 mili giây.

## Bước 2 — Đọc kỹ chỗ gọi API

Thân yêu cầu gửi cho OpenAI chỉ có ba dòng:

```python
{"model": ..., "messages": [...], "max_completion_tokens": ...}
```

Thiếu ba thứ, mỗi thứ là một vấn đề khác nhau:

**Không có `stream`.** `requests.post()` rồi `.json()` — chờ trọn 9.555 token viết xong mới
trả về. Màn hình đứng im 94 giây.

**Không có `reasoning_effort`.** Tra tài liệu OpenAI: không khai báo thì mặc định là
`medium`. Model bỏ ra một lượng token vô hình để nghĩ trước khi viết chữ đầu tiên — người
dùng không đọc được nhưng vẫn chờ và vẫn trả tiền.

**Không đọc `reasoning_tokens`.** Chỉ lấy `completion_tokens` tổng. Nên trong 9.555 token
kia, không ai biết bao nhiêu là bài viết và bao nhiêu là suy nghĩ vứt đi. Không đo được thì
không quyết được nên đặt mức nào.

Thêm một chỗ nữa tìm ra khi soi prompt: `{keyword}` nằm ở **ký tự thứ 284 (2% chiều dài)**.
OpenAI lưu đệm phần đầu prompt nếu nó giống hệt lần trước, nhưng thay từ khóa ở ký tự 284 là
phần đầu đã khác — mất sạch đệm.

## Bước 3 — Kết luận: không phải chậm, mà là không thấy gì

Tool nhiều khả năng **không chậm hơn** ChatGPT về tổng thời gian. Nó chậm hơn về thời gian
ngồi nhìn màn hình trống:

| | ChatGPT | Tool (trước khi sửa) |
|---|---|---|
| Chữ đầu tiên hiện ra | ~3 giây | 94 giây |
| Làm gì trong lúc chờ | Đọc dần | Nhìn màn hình trống |

Chênh nhau 30 lần về cảm giác, gần như không chênh về thời gian thật.

Đã đề nghị người dùng tự kiểm chứng miễn phí: bấm giờ ChatGPT đến lúc **viết xong hẳn**
(không phải lúc chữ đầu hiện ra) rồi đếm số từ. 94 giây cho 3.499 từ có thể còn nhanh hơn
60 giây cho 1.800 từ.

## Bước 4 — Năm việc đã làm

**1. Chữ chạy dần.** Bật `stream` + `stream_options: {include_usage: true}` (không xin thì
gói chữ chạy dần không kèm số token, mất luôn phần đo suy nghĩ). Viết `_doc_dong_chay()` đọc
Server-Sent Events.

Chỗ dễ sai nhất: **luật tkinter**. Luồng nền tuyệt đối không được đụng giao diện. Nên chuỗi
truyền là: provider gọi `khi_co_chu(mẩu chữ)` → hàm này chỉ `queue.put()` → luồng chính
trong `_doc_hang_doi_log()` lấy ra và chèn vào ô soạn thảo. Dùng **hàng đợi riêng** chứ
không dùng chung với hàng đợi log: log là từng dòng có mốc giờ, chữ chạy dần là những mẩu
rời phải nối liền — trộn chung là vỡ cả hai.

Một chi tiết nhỏ mà quan trọng: gom hết mẩu đang chờ rồi mới chèn **một lần**. Mỗi lần chèn
tkinter phải vẽ lại ô, mà 120ms có thể dồn tới vài chục mẩu.

Và `phan_hoi.encoding = "utf-8"` — requests đoán bảng mã từ header, đoán trượt là vỡ hết dấu
tiếng Việt.

**2. Đo token suy nghĩ.** Thêm `token_suy_nghi` vào `KetQua`, ghi ra log kèm phần trăm.

**3. Chọn được mức suy nghĩ.** Ô mới trong Cấu hình AI, chỉ hiện khi dùng OpenAI — hiện cho
Gemini/Claude chỉ tổ làm người dùng tưởng chỉnh được rồi thắc mắc sao không đổi gì.

**Mặc định để trống = không gửi tham số = giữ nguyên hành vi cũ.** Cố ý không tự hạ xuống
`low`: nhanh hơn nhưng chất lượng có thể giảm, mà chưa chạy thật thì không được đổi ngầm.

**4. Đồng hồ đếm giây.** Trạng thái hiện "Đang viết... 42 giây · 1.234 ký tự". Tiện thể sửa
dòng ghi sai "thường mất 20–60 giây" — thật là 72–125 giây. Nhìn thấy số 60 rồi ngồi chờ tới
94 thì đương nhiên thấy chậm.

**5. Chuyển `{keyword}` xuống cuối prompt.** Phần đầu giống nhau giữa hai bài khác nhau:
**284 → 13.347 ký tự**. Phải sửa kèm: câu "Đọc kỹ từ khóa trên" thành "ở cuối file", bỏ
`{keyword}` khỏi khung bài mẫu, và thêm mục "TỪ KHÓA CẦN VIẾT" ở cuối.

## Hai lưới an toàn, vì không chạy thật được

Không gọi API thật nghĩa là không biết OpenAI phản ứng ra sao. Nên thêm hai chỗ đỡ:

- **Bị cấm chữ chạy dần** (vài model / vài tài khoản không cho): tự tắt rồi thử lại. Chờ lâu
  hơn còn hơn không viết được bài nào.
- **Gói SSE vỡ giữa chừng**: bỏ qua gói đó, không làm sập cả bài.

## Kiểm chứng — 43 phép thử, 0 đồng tiền API

Không chạy thật thì phải dựng giả. Hai bộ:

**Bộ 1 (24 phép thử) — phản hồi SSE giả đi qua đúng hàm thật.** Dựng một lớp `PhanHoiGia`
giả `requests.Response` ở đúng những chỗ `_doc_dong_chay()` đụng tới, rồi cho chạy qua hàm
thật. Kiểm: ghép mẩu liền nhau, giữ dấu tiếng Việt, ép utf-8, gọi callback đúng số lần, đọc
token vào/ra/suy nghĩ, đóng kết nối, dòng trống bị bỏ qua, **gói JSON vỡ không làm sập**,
bấm Dừng giữa chừng, chạm giới hạn độ dài, tham số gửi đi đúng trong cả ba trường hợp
(mặc định / chọn low / bị cấm stream), và `.env` gõ bậy thì quay về mặc định.

**Bộ 2 (19 phép thử) — dựng cửa sổ tkinter thật.** Tạo `TabWriter`, bơm chữ qua hàng đợi rồi
kiểm ô soạn thảo nhận đúng; kiểm đồng hồ; kiểm hàng đợi được vét sạch giữa hai lần chạy;
tạo `CuaSoCauHinh` và kiểm ô Mức suy nghĩ ẩn/hiện đúng theo nhà cung cấp, nằm đúng vị trí,
không đẩy khung Thông số tràn khỏi cửa sổ.

Bốn phép thử đầu tiên **báo đỏ**, nhưng soi ra là **test sai chứ không phải code sai**:

- `winfo_ismapped()` luôn trả 0 khi cửa sổ gốc đang `withdraw()`. Phải dùng
  `winfo_manager()` (trả `"pack"` hay `""`) và `deiconify()` trước khi đo tọa độ.
- Test giả định `.env` đang để `openai`, nhưng người dùng đã tự đổi sang `gemini` giữa hai
  lần chạy. Sửa test cho không phụ thuộc vào giá trị hiện tại.

Đây là lý do phải đọc kỹ khi test báo đỏ thay vì sửa code ngay.

## Còn lại

**Chưa đo được tốc độ thật.** Toàn bộ phiên này không gọi OpenAI lần nào. Ghi vào mục "Vấn
đề đang tồn tại" số 10 — việc đầu tiên của phiên sau là chạy thật một bài.

Ba con số cần lấy khi chạy: chữ có chạy ra không, token suy nghĩ chiếm bao nhiêu phần trăm,
và hạ mức xuống `low` thì nhanh hơn bao nhiêu mà điểm SEO có tụt không.
