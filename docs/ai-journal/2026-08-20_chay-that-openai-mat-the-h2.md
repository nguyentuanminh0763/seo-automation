# 2026-08-20 — Chạy thật bằng OpenAI gpt-5-mini và lỗi mất toàn bộ thẻ H2

## Việc cần làm

Phiên trước bàn giao ba việc còn treo về công cụ viết bài:

1. Chưa viết thử bài nào bằng OpenAI `gpt-5-mini` — cần chạy một bài xác nhận.
2. Ba bài thử trước đó đều thiếu external link và thiếu từ khóa ở kết luận. Lời dặn
   trong prompt đã siết nhưng chưa chạy lại để xác nhận.

Hai việc này gộp làm một được: chạy một bài bằng OpenAI rồi chấm bằng `writer/auditor.py`
là biết cả hai câu trả lời cùng lúc.

## Cách làm

Viết một file chạy tạm đi đúng đường code mà giao diện dùng —
`Settings.tu_env()` → `generator.viet_bai()` → `generator.luu_bai()` →
`auditor.kiem_tra()` — để không phải bấm tay qua cửa sổ mà vẫn chạy đúng thứ người dùng
chạy. File này đã xóa sau khi xong, không để lại rác trong repo.

Lưu thêm bản Markdown thô cạnh file HTML để soi được cấu trúc thật, vì bộ kiểm tra chấm
trên Markdown chứ không chấm trên HTML.

## Kết quả lần chạy đầu — đúng là có lỗi, nhưng không phải lỗi đang tìm

OpenAI gọi được ngay, không lỗi kết nối, không lỗi tham số: 72 giây, 6.881 token ra.
Hai mục đang nghi ngờ đều **đạt**: external link 2 link, từ khóa có mặt ở kết bài.

Nhưng bộ kiểm tra báo hai con số vô lý:

```
❌ 3. Số thẻ H2 / H3    chuẩn: H2 ≥ 8    thực tế: 0 H2 / 5 H3
❌ 11. Số câu FAQ       chuẩn: ≥ 5       thực tế: 0 câu
```

Mở bản Markdown ra xem thì thấy nguyên nhân:

```
Cần chuẩn bị gì
- Ổ USB (ít nhất 4 GB) để tạo USB boot MemTest86.
```

`gpt-5-mini` viết tên mục thành **dòng chữ trơn**, không có `##` phía trước. Cả bài chỉ có
đúng một dấu `#` ở tiêu đề và năm dấu `###` ở các câu hỏi FAQ.

## Vì sao đây là lỗi nghiêm trọng

Bài đọc lên vẫn mạch lạc, vẫn đủ mục, vẫn đúng nội dung. Copy sang WordPress cũng dán được.
Nhưng nó ra một trang **không có thẻ H2 nào** — Google không đọc được cấu trúc bài, mất
gần hết giá trị SEO. Đây đúng là loại lỗi mà mắt thường không bắt được và chỉ bộ đếm bằng
code mới lộ ra, giống hệt lý do tháng trước dựng `auditor.py`.

Con số FAQ = 0 chỉ là hệ quả kéo theo. `_dem_faq()` đi tìm dòng heading khớp
`^#{2,3}\s*.*(FAQ|câu hỏi thường gặp)` để định vị khu vực FAQ. Không có `##` thì không tìm
thấy mốc, nên trả về 0 dù năm câu hỏi `###` nằm ngay đó.

## Nguyên nhân gốc

Prompt `giaphongpc-tong-quat.md` chưa bao giờ nói rõ cú pháp heading. Nó chỉ có:

- bảng mục tiêu ghi `| Thẻ H2 | 8–12, dùng H3 để tách ý nhỏ |`
- một dòng ở PHẦN 2: "Toàn văn bài viết dạng Markdown, bắt đầu bằng `# Tiêu đề`"

Gemini tự suy ra "H2" nghĩa là `##`. `gpt-5-mini` thì không. Nặng hơn nữa, ngay phía trên
đó prompt viết in đậm:

> **Không dùng dấu `#` cho hai dòng mốc "PHẦN 1" và "PHẦN 2"**

Câu này nhắm vào đúng hai dòng, nhưng đọc rời ra thì rất dễ hiểu thành "đừng dùng `#`".

**Bài học:** prompt viết cho model này chưa chắc chạy được với model kia. Mọi lần đổi nhà
cung cấp AI đều phải chạy lại một bài rồi soi bằng bộ kiểm tra.

## Cách sửa

Sửa hai chỗ trong `prompts/giaphongpc-tong-quat.md`:

1. Ghi rõ ngoại lệ `#` **chỉ áp dụng cho đúng hai dòng mốc**, còn trong bài vẫn dùng đầy đủ
   `#`, `##`, `###`.
2. Thêm vào PHẦN 2 một bảng cú pháp heading bắt buộc và một khung bài mẫu dạng khối code,
   trong đó có sẵn dòng `## FAQ — Câu hỏi thường gặp` kèm giải thích rằng công cụ dựa vào
   đúng dòng này để đếm FAQ.

Không đụng một dòng code Python nào — đây là lỗi của lời dặn, không phải của công cụ.

## Kết quả sau khi sửa

Chạy lại cùng từ khóa, cùng model:

| | Trước | Sau |
|---|---|---|
| Thẻ H2 | 0 | **11** |
| Câu FAQ | 0 | **5** |
| Mục chưa đạt | 8 / 25 | **5 / 25** |

## Còn tồn lại, không sửa trong phiên này

**Bài ngắn.** 2.061 từ so với chuẩn 3.000. Không phải giới hạn token — mới dùng 7.149 trên
24.000. Đây là văn phong của `gpt-5-mini`, cần đổi model hoặc hạ chuẩn, là quyết định của
người dùng chứ không phải của tôi.

**Cụm lõi từ khóa bóc chưa đủ ngắn.** `lay_tu_khoa_loi()` cắt
"cách kiểm tra ram máy tính có bị lỗi không" xuống còn "kiểm tra ram máy tính có bị lỗi" —
vẫn là một mệnh đề sáu chữ. Đòi lặp mệnh đề đó 15–20 lần và nhét vào ba thẻ H2 là điều
không người viết SEO nào làm. Đo trên bài thật:

| Cụm đếm | Số lần | Mật độ | Số H2 chứa |
|---|---:|---:|---:|
| nguyên từ khóa | 6 | 0,29% | 0 |
| cụm lõi hiện tại (6 chữ) | 7 | 0,34% | 0 |
| `kiểm tra ram` | 14 | 0,68% | 2 |

Nghĩa là bài viết không tệ như bảng điểm nói — cái thước đo mới là thứ cần chỉnh. Đây cùng
một họ lỗi với cái đã sửa lần trước ("đếm nguyên cụm câu hỏi"), chỉ là lần này bóc chưa
đủ tay. Nhưng sửa nó là đổi cách chấm điểm của toàn bộ bài, nên hỏi người dùng trước.

---

# Phần hai — sửa cách chấm mật độ, và so gpt-5 với gpt-5-mini

Người dùng chốt hai việc: bóc cụm lõi ngắn hơn, và chạy thử một bài bằng `gpt-5` để so.

## Bóc cụm lõi: quy tắc vị trí không cứu được

Ý đầu tiên là cắt cứng lấy 3 chữ đầu sau khi bóc chữ hỏi. Đo thử trên ba bài thật thì hỏng
ngay — chỗ đắt của từ khóa không cố định ở đầu:

| Từ khóa | 3 chữ đầu | Cụm bài thực sự bám vào |
|---|---|---|
| cách kiểm tra ram máy tính có bị lỗi không | kiểm tra ram ✅ | `kiểm tra ram` — 14 lần |
| cách khắc phục loa máy tính bàn không nghe được | khắc phục loa ❌ 2 lần | `máy tính bàn` — 8 lần |
| máy tính bị lỗi màn hình xanh recovery | máy tính bị ❌ | `màn hình xanh` — 19 lần |

Nên bỏ hẳn ý đoán theo vị trí. Cách làm cuối cùng: **xét mọi cụm 3 chữ liền nhau trong từ
khóa, chọn cụm được chính bài dùng nhiều nhất**. Đó là đo cái người viết thật sự bám vào,
chứ không phải đoán xem đáng lẽ họ phải bám vào cái gì.

Hàm nhận thêm tham số `noi_dung` để mặc định trống — bỏ trống thì vẫn bóc chữ hỏi rồi lấy
3 chữ đầu như cũ, để chỗ nào gọi mà chưa có bài vẫn chạy được.

Chạy lại ca cũ để chắc không làm hỏng cái đã sửa lần trước: `"cpu hàng tray là gì"` vẫn ra
`"cpu hàng tray"` ✅.

## Nới trần mật độ — vì hai chuẩn tự mâu thuẫn với nhau

Bóc lõi đúng rồi thì hai trong ba bài lại vượt trần 0,55%. Nhìn kỹ mới thấy hai dòng chuẩn
nằm cạnh nhau trong `config.py` **không bao giờ đúng đồng thời được**:

- `tu_khoa_min/max = 15–20 lần`
- `mat_do_min/max = 0,40–0,55%`

15–20 lần trên một bài 2.500 từ là 0,60–0,80%. Đạt mục trên thì trượt mục dưới, và ngược
lại. Đã nới trần lên 0,80%, giữ nguyên sàn 0,40% (15 lần trên bài 4.000 từ là 0,375%).

Đây đúng là điều người dùng nghi từ phiên trước — nhưng lệch **cả hai chiều**, không phải
một chiều như dự đoán ban đầu: từ khóa dài thì tụt dưới sàn, từ khóa ngắn thì vượt trần.

## Một chỗ lệch tìm thấy trên đường đi

`gui/audit_window.py` gọi `tim_cau_nhoi_tu_khoa(noi_dung, self.tu_khoa)` với **nguyên** từ
khóa, trong khi `kiem_tra()` chấm bằng **cụm lõi**. Nghĩa là tab "Câu cần sửa" liệt kê một
danh sách còn bảng điểm hiện một con số khác. Bóc lõi ngắn hơn chỉ làm khoảng lệch rộng ra.

Sửa bằng cách cho `BaoCaoKiemTra` mang sẵn `cau_nhoi` và `so_lieu_nghi_bia`, cửa sổ chỉ đọc
chứ không đếm lại. Bỏ luôn dòng `import auditor` đã thành thừa.

## gpt-5 so với gpt-5-mini

Chấm lại cả hai bài bằng thước đo mới:

| | gpt-5-mini | gpt-5 |
|---|---|---|
| Điểm | **21 đạt / 4 chưa** | 19 đạt / 6 chưa |
| Số từ | 2.061 | 2.460 |
| Thời gian | 79 giây | 125 giây |
| Token ra | 7.149 | 8.474 |

Ngoài dự đoán: `gpt-5` chấm **thấp hơn**. Và mấy mục nó trượt lại nặng hơn — thiếu hẳn khối
author bio, bịa một số liệu — trong khi mini chỉ trượt mấy mục hình thức. Chậm gần gấp đôi
và đắt hơn nhiều lần mỗi bài. Kết luận: không có lý do gì phải đổi.

Nhưng mỗi model mới chạy **một bài**. Đủ để nói "đừng đổi", chưa đủ để nói "mini tốt hơn".

Điểm chung đáng chú ý hơn: **cả hai đều không đạt 3.000 từ**. Cùng thiếu như nhau thì thủ
phạm nhiều khả năng là prompt chưa ép đủ mạnh về độ dài, không phải model.

## Kiểm chứng cuối

- `compileall` sạch, import toàn bộ `gui/` + `writer/` không lỗi
- Dựng thật `CuaSoKiemTra` bằng tkinter rồi `update()` — cửa sổ lên được, không sập
- Danh sách trong tab "Câu cần sửa" nay khớp đúng con số ở bảng điểm (0 câu / 1 chỗ)

---

# Phần ba — ép bài đủ 3.000 từ

Việc còn lại từ phần hai: cả hai model đều chỉ ra 2.100–2.500 từ.

## Thủ phạm là chính prompt, không phải model

Trước khi thêm yêu cầu mới, đọc lại xem prompt đang nói gì về độ dài. Nó nói **được phép
viết ngắn**, và nói tới hai lần:

> Đây là **mục tiêu để nhắm tới**, không phải ràng buộc cứng. Ưu tiên bài đọc trôi chảy;
> lệch vài phần trăm chấp nhận được.

> Lặp ý mục trước là dấu hiệu bài đang bị kéo dài một cách vô ích — **thà ngắn hơn mục tiêu
> còn hơn loãng**.

Không model nào sai cả. Cả hai làm đúng lời dặn. Đây là lần thứ hai trong ngày nguyên nhân
nằm ở lời dặn chứ không ở công cụ — lần đầu là chuyện thiếu `##`.

Bài học chung của cả hai: **trước khi thêm yêu cầu mới, đọc xem prompt đang cho phép cái
ngược lại hay không.** Thêm một câu "phải đủ 3.000 từ" vào bên cạnh hai câu trên thì chỉ tạo
ra mâu thuẫn, model chọn vế nào cũng được.

## Ba phần của cách sửa

**1. Bỏ hai câu cho phép, đổi độ dài thành sàn cứng.** Vẫn giữ ý "đừng lan man", nhưng
chuyển nó thành lời cảnh báo về *chữ đệm* chứ không phải lời cho phép *viết ngắn*.

**2. Ngân sách chữ cho từng khối thay cho mục tiêu tổng.** Đây mới là phần quan trọng. Mô
hình ngôn ngữ không nhẩm nổi "cả bài đã được 3.000 từ chưa" — đã đo rồi, nó tự khai 55 ký tự
trong khi thật 65. Nhưng nó bám được mục tiêu **cục bộ**: viết mục này khoảng 350–450 từ.

| Khối | Ngân sách |
|---|---:|
| Mỗi mục nội dung chính | 350–450 từ × 7–9 mục |
| Mỗi câu FAQ | 60–120 từ × ≥5 |
| Mở bài / Trả lời nhanh | 60–90 từ mỗi khối |
| Checklist | 100–150 từ |
| Kết bài + CTA + đội ngũ | 150–250 từ |

Bảy mục × 350 đã là 2.450, cộng phần còn lại là vừa qua sàn. Prompt nói thẳng luôn rằng nếu
bài thiếu thì gần như chắc chắn do mục nội dung viết mỏng, để model biết chỗ cần bù.

**3. Dạy cách viết dài mà không nhảm.** Ép độ dài mà không nói cách thì model sẽ độn chữ.
Nên liệt kê 5 cách bù hợp lệ, xếp theo thứ tự ưu tiên — đứng đầu là *tách mục lớn thành các
trường hợp cụ thể người đọc thật sự gặp* — và cấm thẳng 4 kiểu chữ đệm quen thuộc ("như đã
biết", "trong thời đại công nghệ hiện nay", đoạn kết nhỏ cuối mỗi mục, liệt kê lợi ích
chung chung).

**Một mâu thuẫn phát sinh phải dọn:** khung bài ở BƯỚC 2 chỉ liệt kê 5–6 mục cho mỗi nhóm,
trong khi phần mới đòi 7–9 mục. Đã thêm ghi chú rằng khung đó là xương sống tối thiểu, thiếu
bao nhiêu thì **tách một mục lớn thành nhiều mục cụ thể hơn** chứ đừng nghĩ thêm chủ đề rời
rạc, kèm ví dụ cụ thể. Nâng luôn chuẩn số H2 từ 8–12 lên 12–14 cho khớp.

## Kết quả

| Lần chạy | Số từ | Điểm |
|---|---:|---|
| Trước khi sửa | 2.061 | 21 đạt / 4 chưa |
| `cách kiểm tra ram máy tính có bị lỗi không` | **3.499** | **22 đạt / 3 chưa** |
| `cách vệ sinh laptop tại nhà an toàn` | **3.071** | 21 đạt / 4 chưa |

Chạy hai từ khóa khác hẳn nhau chứ không lặp lại một từ khóa, để biết chắc không phải ăn may.

## Sửa kèm: bộ bắt số liệu bịa báo oan

Bài mới bị tuýt còi hai câu, soi ra thì cả hai đều oan:

- *"…không dùng **cồn 90%** vì có thể để lại màng bám"* — nồng độ dung dịch
- *"…không tuyệt đối **100%** là RAM hỏng"* — lối nói nhấn mạnh

Cảnh báo sai là cảnh báo bị bỏ qua, mà bị bỏ qua thì cả mục đó thành vô dụng. Đây đúng là
lỗi đã sửa một lần rồi ("bản đầu bắt nhầm 5/5 câu kiểu này") mà bộ lọc còn hẹp.

Lần này sửa cấu trúc chứ không nới danh sách: **gạch bỏ những con số vô hại khỏi câu rồi mới
soi phần còn lại**. Kiểu cũ — thấy số vô hại là tha cả câu — bỏ sót câu vừa có nồng độ vừa
có số bịa thật:

> "dùng cồn 90% để lau, và 65% khách của chúng tôi gặp lỗi này"

Bỏ luôn hàm `_la_cach_noi_quen()` vì cách mới không cần tới nó nữa.

Kiểm bằng 13 câu mẫu — 7 câu phải bỏ qua (nồng độ cồn, độ ẩm, mức pin, "mới 100%") và 6 câu
phải bắt (tỷ lệ trường hợp, hiệu suất tăng, số ca, số lượt khách, câu hỗn hợp). Đúng cả 13.

## Ba mục còn đỏ

Chỉ một cái đáng quan tâm:

| Mục | Đánh giá |
|---|---|
| Độ dài Title / Meta | **Không sửa được bằng prompt.** Mô hình không đếm nổi ký tự. Bộ kiểm tra bắt được, sửa tay 10 giây. Đừng tốn công vì nó |
| Từ khóa trong H2 (bài vệ sinh laptop được 1 thẻ) | Bài RAM đạt 4 thẻ nên chưa rõ là lỗi hệ thống hay do từ khóa |
| Internal link (bài vệ sinh laptop được 4) | Bài RAM đạt 6. Thiếu đúng 1 link |

## Kiểm chứng cuối

- `compileall` sạch, import toàn bộ `gui/` + `writer/` không lỗi
- Dựng thật `CuaSoKiemTra` bằng tkinter trên bài mới — cửa sổ lên được, không sập
- File chạy thử tạm đã xóa

Ghi vào mục "Vấn đề đang tồn tại" số 6–9 trong `PROJECT_STATE.md`.
