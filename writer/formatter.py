# -*- coding: utf-8 -*-
"""
Chuyển bài viết từ Markdown sang HTML để dán vào WordPress.

VÌ SAO TỰ VIẾT THAY VÌ CÀI THƯ VIỆN?
    AI viết bài chỉ dùng vài kiểu định dạng: tiêu đề, in đậm, in nghiêng,
    danh sách, liên kết. Xử lý đúng chừng đó chỉ tốn khoảng 100 dòng, đổi lại
    giữ được nguyên tắc của dự án là không thêm thư viện ngoài, và quan trọng
    hơn là kiểm soát được chính xác thẻ HTML sinh ra — WordPress rất kén.

HTML sinh ra cố ý ĐƠN GIẢN: không class, không style, không thẻ lồng phức tạp.
Càng đơn giản thì WordPress càng chuyển thành khối chuẩn chính xác.
"""

import html
import re
from typing import List

# Nhận diện nội dung AI trả về đã là HTML sẵn (phòng khi prompt yêu cầu vậy)
_DAU_HIEU_HTML = re.compile(r"<(h[1-6]|p|ul|ol|div|article)\b", re.IGNORECASE)


def la_html_san(noi_dung: str) -> bool:
    """Kiểm tra AI đã trả về HTML rồi hay vẫn là Markdown."""
    return bool(_DAU_HIEU_HTML.search(noi_dung[:2000]))


def sang_html(noi_dung: str) -> str:
    """
    Chuyển Markdown sang HTML. Nếu đã là HTML thì trả về nguyên vẹn.
    """
    noi_dung = _don_dep(noi_dung)
    if la_html_san(noi_dung):
        return noi_dung

    cac_the: List[str] = []
    dang_trong_danh_sach = None   # None | "ul" | "ol"
    cac_dong_doan: List[str] = []

    def dong_doan_van():
        """Gom các dòng đang chờ thành một thẻ <p>."""
        if cac_dong_doan:
            cac_the.append(f"<p>{_inline(' '.join(cac_dong_doan))}</p>")
            cac_dong_doan.clear()

    def dong_danh_sach():
        nonlocal dang_trong_danh_sach
        if dang_trong_danh_sach:
            cac_the.append(f"</{dang_trong_danh_sach}>")
            dang_trong_danh_sach = None

    for dong in noi_dung.split("\n"):
        dong_sach = dong.strip()

        # --- Dòng trống: kết thúc đoạn văn đang gom ---
        if not dong_sach:
            dong_doan_van()
            dong_danh_sach()
            continue

        # --- Tiêu đề: # ## ### #### ---
        khop_tieu_de = re.match(r"^(#{1,6})\s+(.*)$", dong_sach)
        if khop_tieu_de:
            dong_doan_van()
            dong_danh_sach()
            cap = len(khop_tieu_de.group(1))
            cac_the.append(f"<h{cap}>{_inline(khop_tieu_de.group(2))}</h{cap}>")
            continue

        # --- Danh sách đánh số: 1. 2. 3. ---
        khop_so = re.match(r"^\d+[.)]\s+(.*)$", dong_sach)
        if khop_so:
            dong_doan_van()
            if dang_trong_danh_sach != "ol":
                dong_danh_sach()
                cac_the.append("<ol>")
                dang_trong_danh_sach = "ol"
            cac_the.append(f"<li>{_inline(khop_so.group(1))}</li>")
            continue

        # --- Danh sách gạch đầu dòng: - hoặc * ---
        khop_gach = re.match(r"^[-*+]\s+(.*)$", dong_sach)
        if khop_gach:
            dong_doan_van()
            if dang_trong_danh_sach != "ul":
                dong_danh_sach()
                cac_the.append("<ul>")
                dang_trong_danh_sach = "ul"
            cac_the.append(f"<li>{_inline(khop_gach.group(1))}</li>")
            continue

        # --- Trích dẫn: > ---
        if dong_sach.startswith(">"):
            dong_doan_van()
            dong_danh_sach()
            cac_the.append(f"<blockquote><p>{_inline(dong_sach.lstrip('> '))}</p></blockquote>")
            continue

        # --- Đường kẻ ngang: --- hoặc *** ---
        if re.match(r"^([-*_])\1{2,}$", dong_sach):
            dong_doan_van()
            dong_danh_sach()
            cac_the.append("<hr>")
            continue

        # --- Còn lại: chữ thường, gom vào đoạn văn ---
        if dang_trong_danh_sach:
            dong_danh_sach()
        cac_dong_doan.append(dong_sach)

    dong_doan_van()
    dong_danh_sach()

    return "\n".join(cac_the)


def _don_dep(noi_dung: str) -> str:
    """
    Bỏ những thứ AI hay thêm thừa: khối mã bao quanh toàn bài, lời dẫn.
    """
    noi_dung = noi_dung.strip()

    # AI đôi khi bọc cả bài trong ```markdown ... ```
    if noi_dung.startswith("```"):
        cac_dong = noi_dung.split("\n")
        if len(cac_dong) > 2:
            cac_dong = cac_dong[1:]
            if cac_dong and cac_dong[-1].strip().startswith("```"):
                cac_dong = cac_dong[:-1]
            noi_dung = "\n".join(cac_dong).strip()

    return noi_dung


def _inline(chu: str) -> str:
    """
    Xử lý định dạng trong dòng: in đậm, in nghiêng, liên kết, mã.

    Thoát ký tự HTML TRƯỚC, rồi mới chèn thẻ — nếu làm ngược lại thì thẻ
    vừa chèn sẽ bị thoát thành chữ.
    """
    chu = html.escape(chu, quote=False)

    # Mã inline `abc` — làm trước để nội dung bên trong không bị hiểu là in đậm
    chu = re.sub(r"`([^`]+)`", r"<code>\1</code>", chu)

    # Liên kết [chữ](địa chỉ)
    chu = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', chu)

    # In đậm **abc** hoặc __abc__
    chu = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", chu)
    chu = re.sub(r"__([^_]+)__", r"<strong>\1</strong>", chu)

    # In nghiêng *abc* hoặc _abc_ (sau in đậm để không ăn nhầm)
    chu = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", chu)
    chu = re.sub(r"(?<!_)_([^_\n]+)_(?!_)", r"<em>\1</em>", chu)

    return chu


def lay_tieu_de(noi_dung: str) -> str:
    """
    Lấy tiêu đề bài viết (dòng # đầu tiên) để đặt tên file.
    Trả về chuỗi rỗng nếu không tìm thấy.
    """
    for dong in noi_dung.split("\n"):
        dong = dong.strip()
        if dong.startswith("#"):
            return dong.lstrip("#").strip()
        if dong.startswith("<h1"):
            khop = re.search(r"<h1[^>]*>(.*?)</h1>", dong, re.IGNORECASE | re.DOTALL)
            if khop:
                return re.sub(r"<[^>]+>", "", khop.group(1)).strip()
    return ""


def dem_tu(noi_dung: str) -> int:
    """Đếm số từ, bỏ qua thẻ HTML và ký hiệu Markdown."""
    chu = re.sub(r"<[^>]+>", " ", noi_dung)
    chu = re.sub(r"[#*_`>\[\]()]", " ", chu)
    return len([t for t in chu.split() if t.strip()])


def boc_trang_html(than_bai: str, tieu_de: str = "") -> str:
    """
    Bọc phần thân thành một trang HTML hoàn chỉnh để mở bằng trình duyệt.

    Đây là đường lui chắc chắn nhất để dán vào WordPress: mở file này bằng
    trình duyệt, Ctrl+A rồi Ctrl+C — trình duyệt sẽ đặt bản có định dạng lên
    clipboard, dán vào WordPress ăn đúng tiêu đề như khi copy từ ChatGPT.
    """
    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<title>{html.escape(tieu_de or "Bài viết")}</title>
<style>
  body {{ font-family: -apple-system, "Segoe UI", Roboto, sans-serif;
         max-width: 760px; margin: 40px auto; padding: 0 20px;
         line-height: 1.7; color: #222; }}
  h1 {{ font-size: 1.9em; }} h2 {{ margin-top: 1.6em; }}
  code {{ background: #f4f4f4; padding: 2px 5px; border-radius: 3px; }}
  blockquote {{ border-left: 4px solid #ddd; margin-left: 0; padding-left: 16px;
               color: #555; }}
</style>
</head>
<body>
{than_bai}
</body>
</html>"""
