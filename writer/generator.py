# -*- coding: utf-8 -*-
"""
Điều phối việc viết bài: ghép prompt -> gọi AI -> chuyển sang HTML -> lưu file.
"""

import os
import re
import unicodedata
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from . import config, formatter
from .logger import lay_log
from .prompts import Prompt
from .providers import KetQua, tao_nha_cung_cap
from .settings import Settings

log = lay_log()


@dataclass
class BaiViet:
    """Một bài viết hoàn chỉnh, sẵn sàng để dán hoặc lưu."""

    keyword: str
    markdown: str
    html: str
    tieu_de: str
    so_tu: int
    so_cho_can_bo_sung: int
    ket_qua_api: KetQua
    # Chuỗi mô tả chi phí, tính sẵn lúc tạo vì giao diện không giữ Settings
    mo_ta_chi_phi: str = ""

    def trang_html_day_du(self) -> str:
        """Trang HTML hoàn chỉnh để mở bằng trình duyệt."""
        return formatter.boc_trang_html(self.html, self.tieu_de)


def viet_bai(keyword: str,
             prompt: Prompt,
             st: Settings,
             ghi_chu_them: str = "") -> BaiViet:
    """
    Viết một bài từ từ khóa. Ném LoiGoiAI nếu API lỗi.
    """
    keyword = (keyword or "").strip()
    if not keyword:
        raise ValueError("Chưa có từ khóa.")

    noi_dung_prompt = prompt.dung_noi_dung(keyword, ghi_chu_them)

    log.info("Đang viết bài cho: %s", keyword)
    log.info("Dùng prompt: %s | AI: %s", prompt.ten, st.mo_ta())

    nha_cung_cap = tao_nha_cung_cap(st)
    ket_qua = nha_cung_cap.viet_bai(noi_dung_prompt)

    markdown = ket_qua.noi_dung
    html = formatter.sang_html(markdown)
    tieu_de = formatter.lay_tieu_de(markdown) or keyword
    so_tu = formatter.dem_tu(markdown)
    so_cho_trong = markdown.count(config.DAU_HIEU_CAN_BO_SUNG)

    log.info("Xong: %d từ · %s", so_tu, ket_qua.mo_ta_chi_phi(st))
    if so_cho_trong:
        log.warning("Bài còn %d chỗ cần bạn điền số liệu thật trước khi đăng.",
                    so_cho_trong)

    return BaiViet(
        keyword=keyword,
        markdown=markdown,
        html=html,
        tieu_de=tieu_de,
        so_tu=so_tu,
        so_cho_can_bo_sung=so_cho_trong,
        ket_qua_api=ket_qua,
        mo_ta_chi_phi=ket_qua.mo_ta_chi_phi(st),
    )


def luu_bai(bai: BaiViet, thu_muc_goc: str) -> str:
    """
    Lưu bài ra file .html trong output/, trả về đường dẫn tuyệt đối.

    Lưu bản HTML đầy đủ (có thẻ <html>) chứ không phải bản Markdown, vì mục
    đích chính là mở bằng trình duyệt rồi copy sang WordPress.
    """
    thu_muc = os.path.join(thu_muc_goc, config.THU_MUC_OUTPUT)
    os.makedirs(thu_muc, exist_ok=True)

    ten = f"{config.OUTPUT_PREFIX}_{_lam_sach_ten(bai.keyword)}_{datetime.now():%Y%m%d_%H%M%S}.html"
    duong_dan = os.path.join(thu_muc, ten)

    with open(duong_dan, "w", encoding="utf-8") as f:
        f.write(bai.trang_html_day_du())

    return os.path.abspath(duong_dan)


def _lam_sach_ten(chu: str, do_dai_toi_da: int = 50) -> str:
    """
    Đổi từ khóa tiếng Việt thành tên file an toàn.
    Ví dụ: "cách kiểm tra ram" -> "cach-kiem-tra-ram"
    """
    # Bỏ dấu tiếng Việt
    chu = unicodedata.normalize("NFD", chu)
    chu = "".join(k for k in chu if unicodedata.category(k) != "Mn")
    chu = chu.replace("đ", "d").replace("Đ", "D")

    chu = re.sub(r"[^a-zA-Z0-9\s-]", "", chu).strip().lower()
    chu = re.sub(r"[\s-]+", "-", chu)

    return chu[:do_dai_toi_da] or "bai-viet"
