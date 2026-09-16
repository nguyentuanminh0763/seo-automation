# SEO Keyword Tools — giaphongpc.vn

Hai công cụ Python tự động thu thập từ khóa SEO cho website bán lẻ máy tính và linh kiện.

| Công cụ | Trả lời câu hỏi | Sản lượng | Tần suất chạy |
|---|---|---|---|
| `trends_scrapper.py` | *Cái gì đang **nóng lên** tuần này?* | 5–10 từ khóa | Hàng tuần |
| `suggest_scrapper.py` | *Người ta **hay hỏi gì**?* | ~7.000 từ khóa | Hàng quý |

---

## Cài đặt

Cần Python 3.9 trở lên.

```bash
python -m pip install -r requirements.txt
```

---

## Giao diện web (mới)

Giao diện chạy trong trình duyệt, dùng cho **hai công cụ thu thập từ khóa**.

```bash
python seo_web.py
```

Trên Windows bấm đúp `Chay_giao_dien_web.bat`. Trình duyệt tự mở; cửa sổ đen là máy chủ,
đóng nó là tắt.

Cần cài thêm hai thư viện (đã có trong `requirements.txt`):

```bash
python -m pip install -r requirements.txt
```

Tính năng:

- Hai màn hình: Google Trends và Google Suggest
- Nhật ký chạy hiện **theo thời gian thực**, không phải chờ xong mới thấy
- Bảng kết quả: tìm nhanh, sắp xếp theo cột, lọc theo nhóm ý định kèm số lượng
- Suggest tính trước **số lượt hỏi Google và số phút** ngay khi bạn sửa danh sách từ khóa
- Nút Dừng giữa chừng, giữ nguyên kết quả đã thu
- Xuất Excel/CSV và tải thẳng về máy
- Nền tối / nền sáng

Đóng tab giữa chừng **không làm dừng lần chạy** — mở lại là thấy tiếp tiến trình.

> **Lưu ý an toàn:** máy chủ chỉ nghe ở `127.0.0.1`, không ai ngoài máy bạn vào được.
> Chi tiết trong [`CLAUDE_RULES.md`](CLAUDE_RULES.md).

### Dành cho người sửa giao diện

Thư mục `web/dist/` là bản đã build, **được commit cố ý** để người dùng không phải cài
Node.js. Sửa `web/src/` xong phải build lại rồi commit cả thư mục `dist/`:

```bash
cd web
npm install
npm run build
```

Muốn vừa sửa vừa xem đổi ngay (hot reload):

```bash
python seo_web.py --dev      # cửa sổ 1
cd web && npm run dev        # cửa sổ 2, mở http://localhost:5173
```

Tài liệu API tự sinh: <http://127.0.0.1:8765/docs>

---

## Giao diện cửa sổ Windows

Ứng dụng cửa sổ Windows dùng cả hai công cụ mà không cần gõ lệnh. Viết bằng `tkinter`
có sẵn trong Python nên **không cần cài thêm thư viện nào**. Đây cũng là giao diện duy
nhất hiện có **tab Viết bài bằng AI** — giao diện web chưa làm phần đó.

```bash
python seo_gui.pyw
```

Trên Windows có thể bấm đúp `Chay_giao_dien.bat`.

Tính năng:

- Hai tab, mỗi tab một công cụ
- Nhập từ khóa trực tiếp, không phải sửa `config.py`
- Xem tiến trình chạy theo thời gian thực
- Bảng kết quả có ô lọc nhanh
- **Nút Dừng giữa chừng, giữ lại toàn bộ kết quả đã thu được**
- Mở thẳng file Excel hoặc thư mục kết quả

> Lưu ý cho người phát triển: luồng nền không được gọi bất kỳ hàm tkinter nào,
> kể cả `widget.after()` — sẽ gây `RuntimeError: main thread is not in main loop`.
> Kết quả được luồng chính thu về qua vòng lặp kiểm tra định kỳ.

---

## 1. `trends_scrapper.py` — Bắt từ khóa đột biến

Dùng Google Trends tìm các truy vấn có mức tăng trưởng **Breakout** (trên 5.000%) trong 30 ngày qua.

```bash
python trends_scrapper.py
python trends_scrapper.py --timeframe "today 3-m" --include-rising
```

Cấu hình: [`trends/config.py`](trends/config.py)

**Kết quả mẫu** (một lần chạy thật):

| Seed Keyword | Breakout Keyword | Tăng trưởng |
|---|---|---:|
| pc gaming | dàn pc gaming | 87.100% |
| laptop gaming | laptop gaming mỏng nhẹ | 81.000% |
| pc gaming | full bộ pc gaming giá rẻ | 72.650% |

### Lưu ý quan trọng

`pytrends` là API **không chính thức**. Google chặn IP khá gắt (HTTP 429). Script đã xử lý:

- Chia lô tối đa 5 từ khóa mỗi lần (giới hạn cứng của Google)
- Nghỉ ngẫu nhiên 5–12 giây giữa các lô
- Retry lũy tiến 60s → 120s → 180s, xoay proxy, đổi User-Agent
- Một lô hỏng chỉ bị bỏ qua, không làm sập cả script

> **Bẫy đã gặp:** không được truyền `retries=` / `backoff_factor=` vào `TrendReq()`.
> pytrends 4.9.2 gọi `urllib3.Retry(method_whitelist=...)`, tham số này đã bị xóa ở
> urllib3 2.x, gây `TypeError` làm hỏng mọi truy vấn.

---

## 2. `suggest_scrapper.py` — Lấy từ khóa làm nội dung

Khai thác Google Suggest (gợi ý tự động của ô tìm kiếm) để lấy hàng nghìn câu hỏi thật người dùng gõ.

```bash
python suggest_scrapper.py            # đầy đủ, ~13 phút
python suggest_scrapper.py --quick    # nhanh gấp 3, bỏ quét bảng chữ cái
```

Cấu hình: [`suggest/config.py`](suggest/config.py)

### Cách hoạt động

Ghép "từ mồi" vào từ khóa gốc rồi hứng toàn bộ gợi ý:

```
"màn hình 2k" + cách      →  cách chỉnh màn hình lên 2k
              + so sánh   →  so sánh màn hình máy tính full hd và 2k
              + là gì     →  màn hình 2k qhd là gì
              + a…z       →  màn hình 2k cũ, màn hình 2k 144hz…
```

Mỗi từ gốc sinh 45 truy vấn, mỗi truy vấn trả về tới 10 gợi ý.

### Kết quả một lần chạy thật

24 từ khóa gốc → **7.045 từ khóa** trong 13,3 phút, xuất Excel chia sẵn theo ý định tìm kiếm:

| Sheet | Số lượng | Dùng làm gì |
|---|---:|---|
| Khắc phục lỗi | 610 | Bài sửa lỗi — dễ lên top nhất |
| Khái niệm | 197 | Bài giải thích thuật ngữ |
| Hướng dẫn | 274 | Bài hướng dẫn từng bước |
| So sánh - Tư vấn | 1.699 | Bài tư vấn chọn mua |
| Thương mại | 1.094 | Trang bán hàng (không viết blog) |
| Thông tin sản phẩm | 3.171 | Trang danh mục |

### Bẫy tiếng Việt đã xử lý

"Máy tính" trong tiếng Việt vừa là *computer* vừa là *máy tính cầm tay Casio*. Không lọc thì
kết quả lẫn đầy `sửa máy tính casio 570` — chiếm khoảng 1,3% dữ liệu. Bộ lọc nằm ở
`TU_KHOA_LOAI_BO` trong [`suggest/config.py`](suggest/config.py).

---

## Cấu trúc mã nguồn

Mỗi file làm đúng một việc, chú thích đầy đủ bằng tiếng Việt.

```
├── trends_scrapper.py      Điểm chạy — chỉ chứa CLI
├── trends/
│   ├── config.py           ★ Hằng số cấu hình — file cần sửa
│   ├── settings.py         Gói cấu hình + tham số dòng lệnh
│   ├── logger.py           Log, ép UTF-8 cho console Windows
│   ├── client.py           Kết nối Google Trends, proxy, User-Agent
│   ├── fetcher.py          Gọi API + retry (toàn bộ logic chống chặn)
│   ├── filters.py          Lọc từ khóa Breakout
│   ├── scanner.py          Điều phối: chia lô → gọi → lọc → gom
│   └── exporter.py         Xuất Excel/CSV
│
├── suggest_scrapper.py     Điểm chạy — chỉ chứa CLI
├── suggest/
│   ├── config.py           ★ Hằng số cấu hình — file cần sửa
│   ├── settings.py         Gói cấu hình + tham số dòng lệnh
│   ├── logger.py           Log, ép UTF-8 cho console Windows
│   ├── expander.py         Sinh biến thể truy vấn từ từ khóa gốc
│   ├── client.py           Gọi Google Suggest + retry
│   ├── classifier.py       Phân loại ý định tìm kiếm
│   ├── collector.py        Điều phối toàn bộ quy trình
│   └── exporter.py         Xuất Excel nhiều sheet
│
├── seo_web.py              Điểm chạy giao diện web
├── webapi/                 API nối giao diện web với ba package trên —
│   ├── config.py           KHÔNG chứa logic thu thập, chỉ gọi lại
│   ├── jobs.py             Quản lý lần chạy nền, cờ dừng, hàng đợi sự kiện
│   ├── runners.py          Gọi quet_breakout() / thu_thap()
│   ├── routes.py           Khai báo đường dẫn API
│   └── server.py           Máy chủ FastAPI + phục vụ file giao diện
├── web/                    Giao diện React (JavaScript thuần, không TypeScript)
│   ├── src/                Mã nguồn — sửa ở đây
│   └── dist/               Bản đã build, ĐƯỢC COMMIT cố ý
│
├── seo_gui.pyw             Điểm chạy giao diện cửa sổ
└── gui/                    Giao diện tkinter — KHÔNG chứa logic thu thập,
    ├── app.py              chỉ gọi lại các hàm trong trends/ và suggest/
    ├── tab_base.py         Khung chung cho hai tab (nhập, chạy, log, kết quả)
    ├── tab_trends.py       Tab Google Trends — chỉ khai báo tùy chọn riêng
    ├── tab_suggest.py      Tab Google Suggest — chỉ khai báo tùy chọn riêng
    ├── widgets.py          Ô log, bảng có lọc, ô nhập từ khóa
    ├── worker.py           Luồng nền, cờ dừng
    └── log_bridge.py       Đưa log lên giao diện an toàn qua hàng đợi
```

Kết quả chạy nằm trong `output/` và **không được đưa lên repo** (xem `.gitignore`).

---

## Hạn chế đã biết

- Google Suggest **không cung cấp lượng tìm kiếm/tháng**. Đây là giới hạn của nguồn miễn phí;
  công cụ trả phí (Ahrefs, Semrush) bán chính dữ liệu đó.
- Google Trends thường trả về **tên thương hiệu đối thủ** trong nhóm Breakout — hữu ích để
  theo dõi thị trường nhưng không dùng làm từ khóa mục tiêu được.
- Cả hai đều dựa trên endpoint không chính thức, Google có thể đổi bất cứ lúc nào.
