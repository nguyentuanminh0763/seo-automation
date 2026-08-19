# -*- coding: utf-8 -*-
"""
Nạp các file prompt do NGƯỜI DÙNG tự viết trong thư mục prompts/.

Nguyên tắc: công cụ không hiểu và không sửa nội dung prompt. Nó chỉ làm
đúng hai việc — thay {keyword} bằng từ khóa, và nối ghi chú thêm vào cuối.
Mọi thứ khác trong file là quyền của người dùng.
"""

import os
from dataclasses import dataclass
from typing import List

from . import config


@dataclass
class Prompt:
    """Một file prompt trong thư mục prompts/."""

    ten: str          # tên hiển thị trên giao diện, vd "giaphongpc"
    duong_dan: str
    noi_dung: str

    def dung_noi_dung(self, keyword: str, ghi_chu_them: str = "") -> str:
        """
        Ghép prompt hoàn chỉnh để gửi cho AI.

        - Thay mọi chỗ {keyword} bằng từ khóa
        - Nếu file KHÔNG có chỗ {keyword} nào, tự thêm từ khóa vào cuối
          (phòng trường hợp người dùng quên đặt)
        - Nối ghi chú thêm vào cuối cùng
        """
        noi_dung = self.noi_dung

        if config.CHO_CHEN_TU_KHOA in noi_dung:
            noi_dung = noi_dung.replace(config.CHO_CHEN_TU_KHOA, keyword)
        else:
            noi_dung = f"{noi_dung}\n\n## Từ khóa cần viết\n\n{keyword}"

        ghi_chu_them = (ghi_chu_them or "").strip()
        if ghi_chu_them:
            noi_dung = (
                f"{noi_dung}\n\n"
                f"## Yêu cầu bổ sung cho riêng bài này\n\n"
                f"{ghi_chu_them}"
            )

        return noi_dung


def liet_ke_prompt(thu_muc_goc: str) -> List[Prompt]:
    """
    Đọc toàn bộ file .md trong thư mục prompts/, sắp xếp theo tên.

    Trả về danh sách rỗng nếu thư mục chưa có hoặc chưa có file nào —
    giao diện sẽ hiện hướng dẫn thay vì báo lỗi.
    """
    thu_muc = os.path.join(thu_muc_goc, config.THU_MUC_PROMPT)
    if not os.path.isdir(thu_muc):
        return []

    danh_sach: List[Prompt] = []
    for ten_file in sorted(os.listdir(thu_muc)):
        if not ten_file.lower().endswith(config.DUOI_FILE_PROMPT):
            continue

        duong_dan = os.path.join(thu_muc, ten_file)
        try:
            with open(duong_dan, "r", encoding="utf-8") as f:
                noi_dung = f.read().strip()
        except OSError:
            continue   # file hỏng hoặc đang bị khóa -> bỏ qua, không làm sập app

        if not noi_dung:
            continue

        danh_sach.append(Prompt(
            ten=os.path.splitext(ten_file)[0],
            duong_dan=duong_dan,
            noi_dung=noi_dung,
        ))

    return danh_sach


def huong_dan_khi_rong(thu_muc_goc: str) -> str:
    """Hiện lên giao diện khi thư mục prompts/ trống."""
    return (
        f"Chưa có file prompt nào trong thư mục:\n"
        f"{os.path.join(thu_muc_goc, config.THU_MUC_PROMPT)}\n\n"
        f"Tạo một file đuôi .md trong đó, viết yêu cầu của bạn, và đặt chữ\n"
        f"{config.CHO_CHEN_TU_KHOA} ở chỗ muốn chèn từ khóa."
    )
