# -*- coding: utf-8 -*-
"""
Xuất báo cáo ra file Excel (.xlsx) hoặc CSV.
"""

import os
from datetime import datetime

import pandas as pd

from .logger import lay_log
from .settings import Settings

log = lay_log()

DO_RONG_COT_TOI_DA = 55  # Giới hạn để cột không bị kéo dài quá tay


def xuat_bao_cao(df: pd.DataFrame, st: Settings) -> str:
    """
    Ghi DataFrame ra file và trả về đường dẫn.

    Excel được ưu tiên (đẹp, ghim tiêu đề, tự giãn cột).
    Nếu thiếu thư viện openpyxl thì tự động chuyển sang CSV thay vì để script chết.
    """
    os.makedirs(st.output_dir, exist_ok=True)
    dau_thoi_gian = datetime.now().strftime("%Y%m%d_%H%M%S")
    ten_goc = f"{st.output_prefix}_{dau_thoi_gian}"

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
    """Ghi Excel có định dạng: ghim dòng tiêu đề và tự giãn độ rộng cột."""
    duong_dan = os.path.join(st.output_dir, f"{ten_goc}.xlsx")

    with pd.ExcelWriter(duong_dan, engine="openpyxl") as writer:
        ten_sheet = "Breakout Keywords"
        df.to_excel(writer, sheet_name=ten_sheet, index=False)
        _gian_cot(writer.sheets[ten_sheet], df)
        writer.sheets[ten_sheet].freeze_panes = "A2"  # Ghim dòng tiêu đề

    return duong_dan


def _gian_cot(sheet, df: pd.DataFrame) -> None:
    """Tự động giãn độ rộng từng cột theo nội dung dài nhất trong cột đó."""
    for chi_so, ten_cot in enumerate(df.columns, start=1):
        do_dai_noi_dung = int(df[ten_cot].astype(str).str.len().max() or 0)
        do_rong = min(max(len(str(ten_cot)), do_dai_noi_dung) + 4, DO_RONG_COT_TOI_DA)
        chu_cai_cot = sheet.cell(row=1, column=chi_so).column_letter
        sheet.column_dimensions[chu_cai_cot].width = do_rong
