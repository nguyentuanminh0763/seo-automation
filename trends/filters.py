# -*- coding: utf-8 -*-
"""
Lọc từ khóa ĐỘT BIẾN (Breakout) từ bảng 'rising' mà Google trả về.

Đây là phần "não" của công cụ - quyết định từ khóa nào đáng đưa vào báo cáo.
"""

from datetime import datetime
from typing import Dict, List, Optional, Tuple

import pandas as pd

from .settings import Settings


def phan_loai_gia_tri(gia_tri, nguong_breakout: int) -> Tuple[str, Optional[float]]:
    """
    Xác định một dòng trong bảng 'rising' có phải Breakout hay không.

    Google trả về cột 'value' ở 2 dạng khác nhau tùy phiên bản pytrends:
        - Chuỗi 'Breakout'      -> tăng trưởng > 5000%
        - Số nguyên (vd 43850)  -> phần trăm tăng trưởng cụ thể
    Hàm này xử lý CẢ HAI, nên không phụ thuộc vào phiên bản pytrends.

    Trả về: (loại_truy_vấn, giá_trị_dạng_số | None)
    """
    if isinstance(gia_tri, str):
        if gia_tri.strip().lower() == "breakout":
            return "Breakout", None
        # Chuỗi kiểu "+1,200%" -> bóc lấy phần số
        so_sach = gia_tri.replace("%", "").replace(",", "").replace("+", "").strip()
        try:
            gia_tri = float(so_sach)
        except ValueError:
            return "Rising", None

    try:
        so = float(gia_tri)
    except (TypeError, ValueError):
        return "Rising", None

    return ("Breakout" if so >= nguong_breakout else "Rising"), so


def loc_breakout(seed_keyword: str,
                 bang_rising: Optional[pd.DataFrame],
                 st: Settings) -> List[Dict]:
    """
    Trích xuất từ khóa đột biến từ bảng 'rising' của MỘT từ khóa hạt giống.

    Tham số:
        seed_keyword : từ khóa hạt giống gốc
        bang_rising  : DataFrame 'rising' do pytrends trả về (cột: query, value)
        st           : Settings, quyết định ngưỡng lọc và chế độ

    Trả về: danh sách dict, mỗi dict là một dòng của báo cáo cuối cùng.
    """
    ket_qua: List[Dict] = []

    # Google có thể trả None hoặc DataFrame rỗng khi từ khóa quá ít lượt tìm.
    if bang_rising is None or not isinstance(bang_rising, pd.DataFrame) or bang_rising.empty:
        return ket_qua
    if "query" not in bang_rising.columns:
        return ket_qua

    thoi_diem = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for thu_hang, dong in enumerate(bang_rising.itertuples(index=False), start=1):
        tu_khoa = str(getattr(dong, "query", "")).strip()
        if not tu_khoa:
            continue

        loai, gia_tri_so = phan_loai_gia_tri(
            getattr(dong, "value", None), st.breakout_threshold
        )

        # --- BỘ LỌC CHÍNH: mặc định chỉ giữ lại Breakout ---
        if loai != "Breakout":
            if not st.include_rising:
                continue
            if gia_tri_so is None or gia_tri_so < st.rising_threshold:
                continue

        ket_qua.append({
            "Seed Keyword": seed_keyword,
            "Breakout Keyword": tu_khoa,
            "Query Type": loai,                 # 'Breakout' hoặc 'Rising'
            "Growth (%)": _dinh_dang_tang_truong(loai, gia_tri_so),
            "Rank": thu_hang,                   # thứ hạng trong bảng rising
            "Geo": st.geo,
            "Timeframe": st.timeframe,
            "Timestamp": thoi_diem,
        })

    return ket_qua


def _dinh_dang_tang_truong(loai: str, gia_tri_so: Optional[float]):
    """Google chỉ ghi nhãn 'Breakout' mà không kèm số -> hiển thị '5000+'."""
    if gia_tri_so is None:
        return "5000+" if loai == "Breakout" else ""
    return int(gia_tri_so)
