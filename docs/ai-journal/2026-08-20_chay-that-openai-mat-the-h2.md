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
đủ tay. Nhưng sửa nó là đổi cách chấm điểm của toàn bộ bài, nên để người dùng chốt.

Ghi vào mục "Vấn đề đang tồn tại" số 6, 7, 8 trong `PROJECT_STATE.md`.
