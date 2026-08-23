# Lộ trình triển khai

> Cập nhật lần cuối: 2026-08-23
>
> **Cách dùng:** đánh dấu `[x]` khi xong, kèm ngày. Việc bỏ thì ghi rõ lý do, đừng xóa —
> để phiên sau không đề xuất lại.
>
> **Đây là danh sách việc tồn.** Người dùng sẽ bảo "đọc lại file này" khi muốn làm.
> Mỗi mục ghi đủ: làm gì · vì sao · file nào · rủi ro. Đừng ghi mơ hồ kiểu "cải thiện X".

---

## ⚡ Mục tiêu gốc — đọc trước khi chọn việc

Tự làm SEO cho **giaphongpc.vn** mà không cần biết lập trình, không cần thuê người:

> **Tìm chủ đề khách đang tìm → viết bài chuẩn SEO → đăng lên web → kéo khách miễn phí.**

Thước đo thành công **không phải** "có bao nhiêu keyword" mà là **có bài đăng đều và có
khách vào web**. Việc nào không đẩy được cây kim đó thì xếp sau.

Câu hỏi cốt lõi khi chọn keyword **không phải** "cái nào nhiều người tìm nhất" mà là
**"cái nào mình thắng được"** — web nhỏ ở TP.HCM không đấu lại chuỗi toàn quốc ở từ rộng.

---

## 🔴 Giai đoạn 0 — CHƯA CHẠY THẬT, làm trước hết

Đây là những thứ đã viết code xong nhưng **chưa xác minh trên thực tế**. Luật dự án cấm
báo hoàn thành khi chưa chạy. Rẻ và nhanh, nhưng **chặn mọi việc khác**.

- [ ] **Chạy thật 1 bài để xem chữ chạy dần có hoạt động không** — *thêm 2026-08-23*
      Đã làm cho OpenAI và Gemini, kiểm bằng 62 phép thử với phản hồi giả, **chưa gọi API
      thật lần nào**. Cần đo: giây thứ mấy chữ đầu tiên hiện ra, log ghi token suy nghĩ
      chiếm bao nhiêu %.
      → File: `writer/providers.py`, `gui/tab_writer.py`
- [ ] **Test nút "Copy để dán WordPress" trên WordPress thật** — *tồn từ 2026-08-19*
      ⚠️ **Đây có thể là chỗ chặn thật sự.** Cả dây chuyền là: từ khóa → xếp ưu tiên →
      viết → **dán lên web**. Khâu cuối chưa ai chạy thử. Hỏng thì mọi việc khác vô nghĩa.
      → File: `writer/clipboard.py` (ghi định dạng "HTML Format" qua Windows API)
- [ ] **Thử mức suy nghĩ `low` rồi so điểm với `medium`** — *thêm 2026-08-23*
      Viết cùng một từ khóa ở hai mức, so số giây và số tiêu chí SEO đạt. Nhanh hơn mà
      điểm không tụt thì giữ luôn.
      → Chỉnh ở nút "Cấu hình AI", ô **Mức suy nghĩ**

---

## Giai đoạn 1 — Thu thập từ khóa ✅ HOÀN THÀNH (2026-08-19)

- [x] Công cụ Google Trends bắt từ khóa Breakout — *2026-08-19*
- [x] Công cụ Google Suggest lấy từ khóa làm nội dung — *2026-08-19*
- [x] Tách module, mỗi file một nhiệm vụ — *2026-08-19*
- [x] Chạy kiểm chứng thật cả hai công cụ — *2026-08-19*
- [x] Đưa lên GitHub — *2026-08-19*
- [x] Dựng hệ thống tài liệu theo dõi tiến độ — *2026-08-19*

---

## Giai đoạn 1b — Giao diện đồ họa ✅ HOÀN THÀNH (2026-08-19)

> **Ghi chú:** mục "giao diện web" từng nằm ở phần *đã quyết định không làm* bên dưới.
> Người dùng yêu cầu lại nên đã triển khai, nhưng chọn **ứng dụng Windows (tkinter)**
> thay vì web — không cần cài thêm thư viện, bấm đúp là chạy.

- [x] Cửa sổ 2 tab cho cả hai công cụ — *2026-08-19*
- [x] Nhập từ khóa trực tiếp, không cần sửa file `config.py` — *2026-08-19*
- [x] Hiển thị tiến trình chạy theo thời gian thực — *2026-08-19*
- [x] Bảng kết quả có ô lọc nhanh — *2026-08-19*
- [x] Nút Dừng giữa chừng, giữ lại kết quả đã thu — *2026-08-19*
- [x] File `.bat` bấm đúp để chạy, không cần gõ lệnh — *2026-08-19*

---

## Giai đoạn 2 — Làm sạch và nâng chất lượng dữ liệu 🔜 TIẾP THEO

Ưu tiên cao, làm được ngay, **không cần công cụ mới, không cần hỏi Google thêm lần nào** —
chạy được ngay trên file 7.045 keyword đã có.

- [ ] ⭐ **Đánh dấu 125 keyword có ý định ĐỊA PHƯƠNG TP.HCM** — *thêm 2026-08-23*
      **Đây là nhóm giá trị nhất đang bị chôn trong file.** Đã đếm thật: 125 keyword
      (1,8%) kiểu `sửa máy tính giá rẻ quận bình thạnh`, `sửa máy tính bàn uy tín ở tphcm`.
      Vì sao đáng nhất: GearVN / CellphoneS / Thế Giới Di Động bán toàn quốc, **không ai
      viết bài riêng cho từng quận**. Người gõ câu đó cần thợ hôm nay và ở gần. Ý định mua
      cao nhất, cạnh tranh thấp nhất, và **thắng được thật**. 125 bài ≈ 4 tháng đăng đều.
      → Thêm cột `Địa phương` + danh sách quận/huyện TP.HCM vào `suggest/config.py`
- [ ] ⭐ **Tách nhóm "Đối thủ" thay vì lọc bỏ** — *ý của người dùng, 2026-08-23*
      Tôi từng đề xuất lọc bỏ tên đối thủ. **Đề xuất đó sai** — làm vậy sẽ xóa mất keyword
      đáng viết nhất. `BUSINESS_OVERVIEW.md` cũng đã ghi "theo dõi thị trường được".
      Đã quét thật: 49 keyword (0,7%) dính tên shop khác, chia làm **3 kiểu**:

      | Kiểu | Ví dụ thật | Dùng để làm gì |
      |---|---|---|
      | Tên trơn | `laptopaz` · `ttg` · `nvt` · `titek` | Tin tình báo — đối thủ có biến, đi xem họ làm gì |
      | Đối thủ + danh mục | `laptop gaming gearvn` · `laptop cũ xgear` · `build pc hoanghapc` | Họ đang **sở hữu liên tưởng** danh mục ↔ thương hiệu. Danh mục anh đang thua |
      | ⭐ Đối thủ + đắn đo | `có nên mua laptop cũ ở cellphones không` | **Viết bài được ngay.** Ý định mua cao nhất toàn bộ dữ liệu |

      Cần thêm **nhóm thứ tư "Cần xem"** cho tên lạ chưa xếp loại (vd `titek` — shop hay
      hãng?). Người dùng xem một lần rồi xếp, danh sách lớn dần.

      ⚠️ **Chỗ khó:** máy không phân biệt được đối thủ với nhà sản xuất. `lenovo` /
      `acer` / `dell` là **hàng đang bán**, `laptopaz` / `titek` là **đối thủ** — nhìn chữ
      không tách được. Bắt buộc hai danh sách khai tay.

      ❓ **Câu hỏi thiết kế chưa chốt:** danh sách đối thủ cả hai tool đều cần. Đặt ở file
      dùng chung (lệch kiến trúc "mỗi tool tự chứa config") hay chép vào cả hai (sớm muộn
      lệch nhau)? Tôi nghiêng về **file dùng chung**, vì đây là dữ liệu *kinh doanh* cùng
      loại với `BUSINESS_OVERVIEW.md`, không phải cấu hình kỹ thuật của từng tool.
- [ ] **Gom cụm topic / cluster** — *thêm 2026-08-23*
      5 keyword `máy tính không bắt được wifi` / `không vào được wifi` / `không hiện wifi`...
      là **một bài**, không phải 5 bài. Đây là việc giá trị cao nhất không cần dữ liệu ngoài,
      và giải đúng vấn đề nhóm "Thông tin sản phẩm" phình 45%.
- [ ] **Đếm số biến thể truy vấn gợi ra mỗi keyword** — *thêm 2026-08-23*
      Keyword được 8 truy vấn khác nhau gợi ra thì "trung tâm" hơn keyword chỉ ra ở 1.
      Tín hiệu miễn phí và trung thực, **code hiện đang vứt bỏ nó** — dict bỏ trùng xong
      là quên số lần gặp. Sửa vài dòng ở `suggest/collector.py`.
      ⚠️ Đây là thứ **thay thế** cho ý "chấm điểm theo vị trí Google Suggest" — xem mục
      "đã cân nhắc và quyết định KHÔNG làm" bên dưới để biết vì sao không dùng vị trí.
- [ ] **Chia nhỏ nhóm "Thông tin sản phẩm"** (đang chiếm 45% — quá lớn)
      → Thêm luật vào `LUAT_PHAN_LOAI` trong `suggest/config.py`
      → Gợi ý tách: theo thương hiệu, theo thông số kỹ thuật, theo dòng sản phẩm
- [ ] **Sửa lỗi xếp nhầm nhóm dịch vụ**
      `mua bán sửa chữa laptop quận bình thạnh` đang bị xếp vào "Khắc phục lỗi"
      → Đảo khối `Thương mại` lên trên khối `Khắc phục lỗi` trong `LUAT_PHAN_LOAI`
- [ ] **Ghi rõ giới hạn của Google Suggest lên file xuất và giao diện** — *thêm 2026-08-23*
      Một dòng: *"Google Suggest không cho biết search volume. Thứ tự trong file là thứ tự
      ưu tiên nội dung, không phải thứ hạng tìm kiếm."* Rẻ, và chặn hiểu nhầm về sau.
- [ ] **Chạy lại `suggest_scrapper.py`** sau khi sửa xong các việc trên, để có file sạch
- [ ] **Thêm cột "Tỉnh khác"** đánh dấu từ khóa gắn tỉnh thành ngoài TP.HCM, để lọc bỏ

---

## Giai đoạn 2b — Nâng cấp tab Trends 🔜

Tab Trends hiện chỉ có 4 cột hữu ích và **không có bộ lọc rác nào** (tab Suggest thì có
`TU_KHOA_LOAI_BO`). Đo thật trên lần chạy 2026-08-21: **2/7 dòng là tên shop đối thủ.**

- [ ] **Tách nhóm đối thủ cho tab Trends** — cùng cơ chế với giai đoạn 2 ở trên
      Xuất Excel 2 sheet: *Từ khóa nội dung* + *Đối thủ*. Sheet đối thủ giữ cột
      `Seed Keyword` vì **chính nó cho biết đối thủ đang mạnh lên ở danh mục nào**.
- [ ] **Thêm cột Intent** — *thêm 2026-08-23*
      Bộ phân loại **đã có sẵn** ở `suggest/classifier.py`. Tab Trends chưa dùng.
      Chỉ là nối dây, không phải viết mới.
- [ ] ⭐ **Trend Direction qua `interest_over_time()`** — *thêm 2026-08-23*
      Tool đang chỉ gọi `related_queries()`. pytrends **có sẵn `interest_over_time()`
      chưa dùng lần nào**.
      Vì sao quan trọng: `rtx 5090` tăng 136.300% — nhưng con số đó **không cho biết bây
      giờ còn tăng hay đã tụt**. Sóng đã chết và sóng đang lên cho ra cùng một Growth %.
      ⚠️ **Đánh đổi thật:** thêm một lượt gọi Google mỗi nhóm → **gấp đôi số lần hỏi** →
      chạy lâu hơn và rủi ro chặn IP cao hơn. Cân nhắc trước khi làm.
      → File: `trends/fetcher.py`
- [ ] **Đổi tên cột `Rank`** — *thêm 2026-08-23*
      Hiện nghĩa là "thứ hạng trong danh sách rising của Google" nhưng đọc lướt rất dễ
      hiểu thành thứ hạng SEO. Đổi thành `Thứ hạng rising` hoặc tương đương.
      → File: `trends/filters.py` dòng 89

---

## Giai đoạn 3 — Nguồn dữ liệu thật để xếp ưu tiên 📋

**Đây là mục tiêu gần người dùng đã nêu:** có 7.045 keyword nhưng không có cột nào để xếp
thứ tự viết bài. Kế hoạch là **tab thứ 4** đọc file xuất từ Ahrefs/GSC, nối Traffic
Potential + KD + vị trí đối thủ vào 7.045 keyword, rồi nối thẳng sang tab Viết bài.

Bài học từ đồng nghiệp SEO (dùng Ahrefs, phân tích đối thủ hacom.vn): **chọn theo Traffic
Potential, không theo Volume** — volume của một cụm chính xác luôn đánh giá thấp cả chủ đề.
Nghiên cứu của Ahrefs xác nhận: biết cả volume lẫn thứ hạng vẫn không tính ra được traffic,
vì một trang top thường xếp hạng cho **khoảng 1.000 keyword liên quan**.

### ❓ Câu chưa trả lời — cần biết trước khi làm gì

> **giaphongpc.vn đã gắn Google Search Console chưa, và web chạy được bao lâu rồi?**

Ba trường hợp dẫn tới ba việc khác hẳn nhau:
- **Đã gắn, web có tuổi** → có sẵn mỏ dữ liệu thật đang nằm không. Làm đầu tiên.
- **Chưa gắn** → gắn ngay, miễn phí, 10 phút. Nhưng chờ 1–2 tháng mới đủ dữ liệu.
- **Web mới, chưa có thứ hạng** → GSC trống rỗng. Cứ viết 125 bài địa phương trước,
  2 tháng sau quay lại đọc GSC.

### Nguồn dữ liệu, xếp theo giá trị

- [ ] ⭐ **Google Search Console** — miễn phí, có API chính thức, là **dữ liệu web của anh**
      Được coi là nguồn đáng tin nhất vì là số thật chứ không phải ước lượng.
      **Mẹo ăn tiền nhất — "striking distance":** lọc keyword web đang xếp hạng **11–20**
      (đầu trang 2). Cải thiện chút là nhảy lên trang 1. Đây chính là bộ lọc "vị trí 14–52"
      đồng nghiệp làm bằng Ahrefs, nhưng **miễn phí và là web của anh** thay vì của đối thủ.
      ⚠️ Hạn chế: chỉ biết keyword web **đã lọt vào top**. Chủ đề chưa viết thì không có gì.
- [ ] **Bing Webmaster Tools** — nguồn volume miễn phí tốt nhất, ít người biết
      Cho **số chính xác, không làm tròn thành khoảng** (vd 1.847 thay vì "1K–10K"),
      **không cần tài khoản quảng cáo**. Có lọc theo quốc gia, ngôn ngữ, và lọc riêng
      câu hỏi.
      ⚠️ Bing chỉ ~3% thị phần → coi là **chỉ dấu tương đối** cho nhu cầu trên Google.
- [ ] **Ahrefs qua đồng nghiệp** — kênh đã có sẵn, chỉ cần xin file export
      Traffic Potential là chỉ số đúng. **Không cần mua gói riêng.**
- [ ] **Tab 4 — đọc file Ahrefs/GSC và nối vào 7.045 keyword** ← mục tiêu gần
      Chặn ở: chưa có file dữ liệu.
- [ ] Đối chiếu: nhóm ý định nào thực sự ra traffic, có đúng thứ tự ưu tiên đang giả định không
- [ ] Ghi kết quả vào `docs/RESULTS_LOG.md` phần "Chỉ số cần theo dõi về sau"

---

## Giai đoạn 3b — Chấm điểm và xếp hạng keyword 📋 CHỜ DỮ LIỆU

**Chỉ làm SAU khi giai đoạn 3 có dữ liệu thật.** Lý do ở mục "KHÔNG làm" bên dưới.

- [ ] **Keyword Opportunity Score** — điểm tổng hợp từ nhiều tín hiệu
      Chỉ có ý nghĩa khi đã có Volume / Competition / Traffic Potential thật.
      Khi làm, phải **hiển thị rõ từng thành phần** để người dùng biết vì sao keyword
      được ưu tiên, và phải **chuẩn hóa thang đo** trước khi cộng.
- [ ] **Tách rõ 2 bước: Keyword Discovery và Keyword Prioritization**
      Bước 1 (Suggest/Trends) thu càng nhiều càng tốt → Bước 2 chuẩn hóa, bỏ trùng, gom
      cụm, chấm điểm, xếp hạng. Đúng về nguyên tắc, nhưng chỉ tách khi đã có bước 2 thật.
- [ ] **So sánh giữa các lần chạy theo thời gian** (7 / 30 / 90 ngày)
      Keyword mới xuất hiện · keyword biến mất · Trend tăng/giảm · đối thủ nào đang lên đều.
      `Timestamp` đã lưu sẵn nên rẻ. Giá trị thật của sheet Đối thủ nằm ở đây.

---

## Giai đoạn 3c — Tab Viết bài, việc còn tồn 📋

- [ ] **Điền đơn giá OpenAI vào `BANG_GIA`** trong `writer/config.py`
      Hiện ô chi phí chỉ hiện số token, không hiện tiền. Lấy đơn giá ở trang billing.
- [ ] **Chữ chạy dần cho Claude** — chưa làm vì `ANTHROPIC_API_KEY` đang trống,
      không kiểm chứng được. ⚠️ Bẫy: `thinking.budget_tokens` đã bị khai tử ở Claude 4.6
      và **bị từ chối thẳng từ 4.7 trở lên**, trong khi mặc định dự án là `claude-opus-5`.
      Model đời mới dùng `effort`.
- [ ] **Chọn mức suy nghĩ cho Gemini** — Gemini gọi là `thinkingLevel` (không phải
      `reasoning_effort`). Hiện chỉ OpenAI chỉnh được.
- [ ] **Theo dõi: từ khóa trong H2 và internal link chưa ổn định**
      Bài RAM đạt (4 thẻ H2 / 6 link), bài vệ sinh laptop trượt (1 thẻ / 4 link).
      Chưa rõ lỗi hệ thống hay do đặc điểm từ khóa — cần thêm vài bài mới kết luận.
- [ ] ~~Độ dài Title/Meta luôn vượt chuẩn~~ — **KHÔNG sửa được bằng prompt.**
      Mô hình không đếm nổi ký tự (tự khai 55 trong khi thật 65). Bộ kiểm tra đã bắt được,
      sửa tay 10 giây trước khi đăng. **Đừng tốn công sửa prompt vì mục này.**

---

## Giai đoạn 4 — Mở rộng công cụ 💡 Ý TƯỞNG

Chưa cam kết. Cân nhắc khi giai đoạn 2 và 3 đã ổn.

- [ ] **People Also Ask** — lấy phần "Mọi người cũng hỏi" của Google
      ⚠️ Rủi ro: dễ bị chặn IP hơn Suggest nhiều, cần cân nhắc kỹ
- [ ] **Theo dõi thứ hạng từ khóa** — kiểm tra vị trí của giaphongpc.vn theo thời gian
- [x] ~~**So sánh giữa các lần chạy**~~ — chuyển lên **giai đoạn 3b** *(2026-08-23)*,
      vì nó gắn với việc theo dõi đối thủ theo thời gian chứ không còn là ý tưởng rời
- [ ] **Tự động chạy hàng tuần** — Task Scheduler của Windows chạy `trends_scrapper.py`
- [ ] **Gộp kết quả nhiều lần chạy** — hiện mỗi lần tạo file riêng, chưa có bản tổng hợp

---

## Đã cân nhắc và quyết định KHÔNG làm

| Việc | Lý do bỏ |
|---|---|
| Chuyển sang database (SQLite/Postgres) | Người dùng làm SEO, không phải lập trình viên. Excel là định dạng họ dùng hàng ngày |
| ~~Giao diện web~~ | ĐÃ ĐẢO QUYẾT ĐỊNH 2026-08-19: người dùng yêu cầu giao diện. Đã làm bằng tkinter (ứng dụng Windows) thay vì web, để không phải cài thêm thư viện |
| ~~Dùng API trả phí (Ahrefs, Semrush)~~ | ĐÃ ĐIỀU CHỈNH 2026-08-23: vẫn **không mua gói riêng**, nhưng **đồng nghiệp có Ahrefs** nên sẽ xin file export rồi nhập vào tab 4. Không cần API |
| Gộp hai công cụ làm một | Chúng trả lời hai câu hỏi khác nhau, tần suất chạy khác nhau. Tách riêng dễ hiểu hơn |
| Dùng lớp retry sẵn của pytrends | Không tương thích urllib3 2.x. Retry tự viết kiểm soát tốt hơn |
| **Google Ads Keyword Planner** *(2026-08-23)* | Nghiên cứu trên 72.635 keyword: **thổi phồng volume 54% số trường hợp** vì gộp các cụm gần nghĩa rồi cộng dồn. Ngoài ra **không có API cho dữ liệu volume** nên không nhét vào tool được. Cần tài khoản Ads mà đổi lại số liệu kém tin |
| **Chấm điểm keyword theo vị trí Google Suggest** *(2026-08-23)* | Xem mục "đã đánh giá" bên dưới. Con số sẽ vô nghĩa ở kiến trúc này |
| **Lọc bỏ tên đối thủ** *(2026-08-23)* | Từng đề xuất rồi **rút lại**. Làm vậy sẽ xóa mất `có nên mua laptop cũ ở cellphones không` — keyword ý định mua cao nhất trong file. Phải **tách riêng**, không xóa |

---

## Đã đánh giá góp ý từ AI khác — đừng bàn lại 🧾

*Ghi 2026-08-23. Người dùng đưa xem hai bản góp ý (ChatGPT). Đã review đối chiếu code thật.*

### Bản 1 — về tab Suggest (10 mục)

| Mục | Kết luận |
|---|---|
| Đổi tên trường `SEO Rank` / `Search Volume` / `Ranking` | ❌ **Sai tiền đề.** Đã grep cả dự án: tab Suggest **không có trường nào như vậy**, và **không hề ghi lại vị trí Google Suggest**. Cột thật: `Keyword chính · Nhóm ý định · Loại bài đề xuất · Từ khóa gốc · Số từ · Truy vấn nguồn · Timestamp`. Bảng sắp xếp theo nhóm ý định → độ dài → chữ cái |
| Tạo Suggest Score từ vị trí (#1→100, #2→90...) | ❌ **Con số sẽ vô nghĩa.** Mỗi seed sinh **45 biến thể truy vấn**, một keyword xuất hiện ở nhiều biến thể, dict giữ lần gặp đầu. Nên `position=1` nghĩa là "vị trí #1 của cái biến thể tình cờ chạy trước" — phụ thuộc thứ tự vòng lặp. Tệ hơn: vị trí #1 của truy vấn hẹp `địa chỉ bán máy tính x` được 100đ, còn vị trí #6 của truy vấn rộng `máy tính` chỉ 50đ — **ngược hoàn toàn thực tế**. Dùng "đếm số biến thể gợi ra" thay thế |
| Keyword Opportunity Score | ❌ **Tự mâu thuẫn với chính mục 10 của nó.** Mục 10 bảo đừng coi Suggest #1 là volume, nhưng mục 3 lại xây điểm số mà **thành phần có thật duy nhất chính là vị trí Suggest đó**. Kiểm 8 thành phần: chỉ **1/8 có dữ liệu** (Intent). Cộng 8 thứ mà 7 bằng 0 thì kết quả là cái thứ nhất đội lốt công thức. Nguy hiểm hơn vì "Opportunity Score: 87" trông như sự thật đã tính toán. Công thức còn cộng thẳng các thang đo khác nhau, không chuẩn hóa |
| Bổ sung Search Volume thật, không được fake | ✅ Đúng → giai đoạn 3 |
| Gom cụm topic/intent | ✅✅ **Đúng nhất, giá trị cao nhất** → giai đoạn 2 |
| Tách Discovery / Prioritization | ✅ Đúng nguyên tắc → giai đoạn 3b |
| Theo dõi theo thời gian | ✅ Đúng, rẻ → giai đoạn 3b |
| Không coi Suggest #1 = volume cao nhất | ✅ Đúng — nhưng **tool chưa bao giờ làm vậy** |

**Tổng kết bản 1:** đúng về **đích đến**, sai về **thứ tự** — muốn dựng tầng chấm điểm
trước khi có dữ liệu để chấm.

### Bản 2 — về tab Trends

Đề xuất thêm `Trend Score + Search Volume + Competition + CPC + Intent + Trend Direction`.
Chính nó viết `???` cho 4/6 cột — tức tự thừa nhận không có dữ liệu.

| Cột | Kết luận |
|---|---|
| Intent | ✅ Làm được ngay, classifier có sẵn → giai đoạn 2b |
| Trend Direction | ✅✅ **Ý hay nhất**, `interest_over_time()` có sẵn chưa dùng → giai đoạn 2b |
| Trend Score | ⚠️ Chỉ là đổi thang đo của Growth %, giá trị thấp |
| Search Volume | ❌ **Google Trends về bản chất không cung cấp** — nó chỉ đưa chỉ số tương đối 0–100. Không phải giới hạn của tool, là bản chất sản phẩm |
| CPC / Competition | ❌ Cần Google Ads hoặc Ahrefs → giai đoạn 3 |

**Cả hai bản đều bỏ sót** điều dữ liệu của chính người dùng chứng minh: 2/7 dòng Breakout
là tên shop đối thủ, và `BUSINESS_OVERVIEW.md` đã có luật xử lý mà **chưa đưa vào code**.
Thêm cột Volume/CPC bên cạnh dòng `laptopaz` không giúp gì.
