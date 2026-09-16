# -*- coding: utf-8 -*-
"""
Đổi kết quả của công cụ sang JSON để trình duyệt đọc được.

VÌ SAO TÁCH RIÊNG FILE NÀY?
    DataFrame của pandas chứa kiểu dữ liệu riêng (numpy.int64, NaN, Timestamp)
    mà json.dumps không hiểu — ném TypeError giữa chừng. Gom hết chỗ chuyển đổi
    vào một file để khi thêm cột mới chỉ phải sửa một nơi.
"""

import math
from typing import Any, Dict, List

# Số dòng gửi về trình duyệt tối đa trong một lần. Suggest ra tới 7.000 dòng;
# nhồi hết một lượt thì trang đơ vài giây lúc dựng bảng. Phần còn lại vẫn nằm
# nguyên trong file Excel xuất ra — không mất dữ liệu, chỉ là không hiện hết.
SO_DONG_GUI_TOI_DA = 3000


def _gia_tri(o: Any) -> Any:
    """Đổi một ô dữ liệu sang kiểu JSON hiểu được."""
    # NaN / NaT: pandas dùng cho ô trống. json.dumps đổi thành NaN — sai cú pháp
    # JSON, trình duyệt sẽ báo lỗi phân tích.
    if o is None:
        return ""
    if isinstance(o, float) and (math.isnan(o) or math.isinf(o)):
        return ""
    if isinstance(o, (str, int, bool)):
        return o
    if isinstance(o, float):
        return o
    # numpy.int64 và bạn bè đều có .item() trả về kiểu Python thuần.
    if hasattr(o, "item"):
        try:
            return _gia_tri(o.item())
        except Exception:  # noqa: BLE001
            pass
    return str(o)


def bang_du_lieu(df, gioi_han: int = SO_DONG_GUI_TOI_DA) -> Dict[str, Any]:
    """
    Đổi DataFrame sang {cot, dong, tong_dong, da_cat}.

    `tong_dong` là số dòng THẬT, `dong` có thể ít hơn nếu bị cắt bớt. Giao diện
    phải nói rõ chỗ này cho người dùng, không được để họ tưởng mất dữ liệu.
    """
    if df is None or len(df) == 0:
        return {"cot": [], "dong": [], "tong_dong": 0, "da_cat": False}

    cot = [str(c) for c in df.columns]
    phan_hien = df.head(gioi_han)

    dong: List[List[Any]] = []
    for bo in phan_hien.itertuples(index=False, name=None):
        dong.append([_gia_tri(o) for o in bo])

    return {
        "cot": cot,
        "dong": dong,
        "tong_dong": int(len(df)),
        "da_cat": bool(len(df) > len(phan_hien)),
    }


def dem_theo_cot(df, ten_cot: str) -> List[Dict[str, Any]]:
    """Đếm số dòng theo từng giá trị của một cột, để vẽ ô thống kê."""
    if df is None or len(df) == 0 or ten_cot not in df.columns:
        return []
    dem = df[ten_cot].value_counts()
    return [{"ten": str(k), "so_luong": int(v)} for k, v in dem.items()]
