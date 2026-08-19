# -*- coding: utf-8 -*-
"""
Xuất báo cáo ra Excel nhiều sheet (hoặc CSV).

File Excel được chia sẵn theo nhóm ý định, mỗi nhóm một sheet, để bạn giao việc
cho người viết bài mà không phải lọc lại bằng tay.
"""

import os
import re
from datetime import datetime

import pandas as pd

from .classifier import uu_tien_content
from .logger import lay_log
from .settings import Settings

log = lay_log()

DO_RONG_COT_TOI_DA = 60
COT_TOM_TAT = ["Keyword chính", "Loại bài đề xuất", "Từ khóa gốc", "Số từ"]


def xuat_bao_cao(df: pd.DataFrame, st: Settings) -> str:
    """Ghi DataFrame ra file, trả về đường dẫn tuyệt đối."""
    os.makedirs(st.output_dir, exist_ok=True)
    ten_goc = f"{st.output_prefix}_{datetime.now():%Y%m%d_%H%M%S}"

    if st.output_format == "csv":
        return os.path.abspath(_xuat_csv(df, st, ten_goc))

    try:
        return os.path.abspath(_xuat_excel(df, st, ten_goc))
    except ImportError:
        log.warning("Thiếu thư viện openpyxl (pip install openpyxl) -> chuyển sang CSV.")
        return os.path.abspath(_xuat_csv(df, st, ten_goc))


def _xuat_csv(df: pd.DataFrame, st: Settings, ten_goc: str) -> str:
    """Ghi CSV với encoding utf-8-sig để mở bằng Excel không lỗi font tiếng Việt."""
    duong_dan = os.path.join(st.output_dir, f"{ten_goc}.csv")
    df.to_csv(duong_dan, index=False, encoding="utf-8-sig")
    return duong_dan


def _xuat_excel(df: pd.DataFrame, st: Settings, ten_goc: str) -> str:
    """
    Ghi Excel gồm:
        - Sheet "Tổng hợp"  : toàn bộ keyword
        - Mỗi nhóm ý định   : một sheet riêng (Khắc phục lỗi, Khái niệm, Hướng dẫn...)
    """
    duong_dan = os.path.join(st.output_dir, f"{ten_goc}.xlsx")

    with pd.ExcelWriter(duong_dan, engine="openpyxl") as writer:
        # --- Sheet tổng hợp ---
        df.to_excel(writer, sheet_name="Tổng hợp", index=False)
        _dinh_dang_sheet(writer.sheets["Tổng hợp"], df)

        # --- Mỗi nhóm ý định một sheet, xếp theo độ ưu tiên làm content ---
        cac_nhom = sorted(df["Nhóm ý định"].unique(), key=uu_tien_content)
        for nhom in cac_nhom:
            df_nhom = df[df["Nhóm ý định"] == nhom][COT_TOM_TAT].reset_index(drop=True)
            ten_sheet = _lam_sach_ten_sheet(nhom)
            df_nhom.to_excel(writer, sheet_name=ten_sheet, index=False)
            _dinh_dang_sheet(writer.sheets[ten_sheet], df_nhom)

    return duong_dan


def _lam_sach_ten_sheet(ten: str) -> str:
    """Excel cấm các ký tự : \\ / ? * [ ] trong tên sheet và giới hạn 31 ký tự."""
    ten_sach = re.sub(r"[:\\/?*\[\]]", "-", ten)
    return ten_sach[:31]


def _dinh_dang_sheet(sheet, df: pd.DataFrame) -> None:
    """Ghim dòng tiêu đề và tự giãn độ rộng cột theo nội dung."""
    sheet.freeze_panes = "A2"
    for chi_so, ten_cot in enumerate(df.columns, start=1):
        do_dai = int(df[ten_cot].astype(str).str.len().max() or 0)
        do_rong = min(max(len(str(ten_cot)), do_dai) + 4, DO_RONG_COT_TOI_DA)
        sheet.column_dimensions[sheet.cell(row=1, column=chi_so).column_letter].width = do_rong
