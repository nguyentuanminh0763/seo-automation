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


def bao_cao_seo(bao_cao) -> Dict[str, Any]:
    """Đổi BaoCaoKiemTra của writer/auditor.py sang JSON."""
    return {
        "tom_tat": bao_cao.tom_tat(),
        "so_dat": bao_cao.so_dat,
        "so_chua_dat": bao_cao.so_chua_dat,
        "so_can_kiem": bao_cao.so_can_kiem,
        "so_cham_duoc": bao_cao.so_cham_duoc,
        "pham_vi_dem": bao_cao.pham_vi_dem,
        "tu_khoa_loi": bao_cao.tu_khoa_loi,
        "cau_nhoi": list(bao_cao.cau_nhoi),
        "so_lieu_nghi_bia": list(bao_cao.so_lieu_nghi_bia),
        "cac_muc": [
            {
                "ten": m.ten,
                "chuan": m.chuan,
                "thuc_te": m.thuc_te,
                "trang_thai": m.trang_thai,
                "bieu_tuong": m.bieu_tuong,
                "goi_y": m.goi_y,
            }
            for m in bao_cao.cac_muc
        ],
    }


def bai_viet(bai) -> Dict[str, Any]:
    """Đổi BaiViet của writer/generator.py sang JSON."""
    return {
        "keyword": bai.keyword,
        "tieu_de": bai.tieu_de,
        "so_tu": bai.so_tu,
        "so_cho_can_bo_sung": bai.so_cho_can_bo_sung,
        "mo_ta_chi_phi": bai.mo_ta_chi_phi,
        "markdown": bai.markdown,
        "html": bai.html,
        "token_vao": bai.ket_qua_api.token_vao,
        "token_ra": bai.ket_qua_api.token_ra,
        "token_suy_nghi": bai.ket_qua_api.token_suy_nghi,
    }
