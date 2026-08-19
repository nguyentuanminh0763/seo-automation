# SEO AI WORKFLOW GUIDE

> File này giải thích cách làm việc với dự án. Đọc file này đầu tiên khi tiếp quản dự án.

---

## Tổng quan dự án

Bộ công cụ Python tự động thu thập từ khóa SEO cho **giaphongpc.vn** — website bán lẻ
máy tính, laptop và linh kiện tại TP.HCM.

Hai công cụ độc lập, trả lời hai câu hỏi khác nhau:

| Công cụ | Trả lời | Sản lượng | Tần suất chạy |
|---|---|---|---|
| `trends_scrapper.py` | *Cái gì đang **nóng lên** tuần này?* | 5–10 từ khóa | Hàng tuần |
| `suggest_scrapper.py` | *Người ta **hay hỏi gì**?* | ~7.000 từ khóa | Hàng quý |

Bối cảnh kinh doanh chi tiết: [`docs/BUSINESS_OVERVIEW.md`](docs/BUSINESS_OVERVIEW.md)

---

## Cấu trúc dự án

```txt
seo/
│
├── CLAUDE.md                     Bootstrap tự động cho Claude Code
├── CLAUDE_RULES.md               ★ Luật làm việc bền vững — ĐỌC TRƯỚC KHI SỬA
├── PROJECT_STATE.md              ★ Hiện trạng + lịch sử cập nhật
├── SEO_AI_WORKFLOW_GUIDE.md      File này
├── implementation_plan.md        Lộ trình các bước tiếp theo
├── README.md                     Giới thiệu công khai trên GitHub
├── requirements.txt              Danh sách thư viện
│
├── trends_scrapper.py            Điểm chạy công cụ 1 — chỉ chứa CLI
├── trends/                       Logic công cụ 1 (9 file, mỗi file 1 việc)
│   └── config.py                 ★ File người dùng sửa
│
├── suggest_scrapper.py           Điểm chạy công cụ 2 — chỉ chứa CLI
├── suggest/                      Logic công cụ 2 (9 file, mỗi file 1 việc)
│   └── config.py                 ★ File người dùng sửa
│
├── docs/
│   ├── BUSINESS_OVERVIEW.md      Bối cảnh giaphongpc.vn
│   ├── RESULTS_LOG.md            ★ Nhật ký kết quả từng lần chạy
│   └── ai-journal/               Báo cáo chi tiết từng phiên làm việc
│
└── output/                       Kết quả Excel — KHÔNG commit lên git
```

---

## Các file quan trọng

### 1. `CLAUDE_RULES.md`
Luật làm việc không đổi: nguyên tắc kiến trúc, các bẫy kỹ thuật đã gặp, điều tuyệt đối tránh.
**Luôn đọc trước khi sửa code.**

### 2. `PROJECT_STATE.md`
Hiện trạng dự án: cái gì đã xong, kết quả đo được, vấn đề đang tồn tại.
**Luôn cập nhật sau khi thay đổi.**

### 3. `docs/RESULTS_LOG.md`
Nhật ký từng lần chạy công cụ: ngày giờ, tham số, số keyword thu được, thời gian, ghi chú.
Đây là chỗ theo dõi **hiệu quả** — chạy lần này có tốt hơn lần trước không.

### 4. `docs/ai-journal/`
Mỗi phiên làm việc lớn ghi một file. Đặt tên `YYYY-MM-DD_mo-ta-ngan.md`.
Ghi lại: đã làm gì, tại sao, lỗi gì đã gặp, kiểm chứng ra sao.

### 5. `implementation_plan.md`
Lộ trình. Việc nào đang làm, việc nào chờ, việc nào đã bỏ và vì sao.

---

## Bắt đầu một phiên AI mới

### Với Claude Code
File `CLAUDE.md` tự động được nạp. Không cần làm gì thêm.

### Với AI khác (ChatGPT, Gemini, Copilot...)
Dán đoạn này vào đầu cuộc trò chuyện:

```
Đây là phiên tiếp nối dự án SEO Automation cho giaphongpc.vn.

Trước khi thay đổi bất cứ thứ gì, hãy đọc:
- CLAUDE_RULES.md      (luật làm việc, các bẫy kỹ thuật đã gặp)
- PROJECT_STATE.md     (hiện trạng, vấn đề đang tồn tại)
- docs/RESULTS_LOG.md  (kết quả các lần chạy trước)
- docs/ai-journal/     (nhật ký chi tiết)

KHÔNG viết lại từ đầu. KHÔNG gộp package về một file.
KHÔNG chuyển sang TypeScript hay thêm database.
Chỉ cải tiến từng phần nhỏ.

Người dùng KHÔNG biết lập trình — giải thích bằng tiếng Việt,
đưa lệnh đầy đủ có thể copy-paste ngay.
```

---

## Quy trình chuẩn cho mỗi nhiệm vụ

**1. ĐỌC BỐI CẢNH**
`CLAUDE_RULES.md` → `PROJECT_STATE.md` → journal liên quan

**2. KIỂM TRA HIỆN TRẠNG**
Xem code thật, xác định file bị ảnh hưởng và mức rủi ro

**3. ĐỀ XUẤT KẾ HOẠCH**
Nói rõ sửa gì, file nào, rủi ro ra sao. Chờ xác nhận nếu rủi ro trung bình trở lên

**4. LÀM NHỎ**
Không viết lại lớn. Từng bước một

**5. CHẠY THẬT ĐỂ KIỂM CHỨNG**
> Đây là bước quan trọng nhất. Dự án này đã có 3 lỗi chỉ lộ ra khi chạy thật,
> không lỗi nào phát hiện được bằng cách đọc code.
> **Không bao giờ báo "đã xong" khi chưa chạy.**

**6. GHI LẠI**
Cập nhật `PROJECT_STATE.md` → thêm file vào `docs/ai-journal/` →
ghi số liệu vào `docs/RESULTS_LOG.md` nếu có chạy công cụ

---

## Lệnh hay dùng

Python không nằm trong PATH, phải gọi đường dẫn đầy đủ:

```bash
"C:\Users\PC\AppData\Local\Programs\Python\Python312\python.exe" trends_scrapper.py
```

```bash
"C:\Users\PC\AppData\Local\Programs\Python\Python312\python.exe" suggest_scrapper.py --quick
```

Cài lại thư viện:

```bash
"C:\Users\PC\AppData\Local\Programs\Python\Python312\python.exe" -m pip install -r requirements.txt
```

Đẩy thay đổi lên GitHub:

```bash
git add -A && git commit -m "Mô tả thay đổi" && git push
```

---

## Ba bẫy đã gặp thật — đừng vấp lại

1. **`pytrends` × `urllib3` 2.x** — không truyền `retries=` vào `TrendReq()`, sẽ vỡ toàn bộ truy vấn
2. **Console Windows cp1252** — phải ép stdout sang UTF-8, không thì log tiếng Việt vỡ hết
3. **Push git qua SSH** — khóa SSH trên máy thuộc tài khoản khác, luôn dùng remote HTTPS

Chi tiết trong `CLAUDE_RULES.md`.
