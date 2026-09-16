# -*- coding: utf-8 -*-
"""
Hai hàm chạy thật, gọi lại code có sẵn trong trends/ và suggest/.

NGUYÊN TẮC:
    File này KHÔNG chứa logic thu thập. Nó chỉ dựng Settings từ tùy chọn người
    dùng gõ trên web, gọi đúng hàm mà bản dòng lệnh và bản tkinter vẫn gọi, rồi
    đóng gói kết quả. Muốn đổi cách thu thập thì sửa trends/ hoặc suggest/.

VÌ SAO NHẬP THƯ VIỆN BÊN TRONG HÀM CHỨ KHÔNG Ở ĐẦU FILE?
    pandas và pytrends mất khoảng một giây để nạp, và nếu người dùng chưa chạy
    `pip install -r requirements.txt` thì nạp sẽ ném lỗi. Nhập ở đầu file nghĩa
    là máy chủ không khởi động nổi và người dùng chỉ thấy cửa sổ đen tắt ngóm.
    Nhập trong hàm thì máy chủ vẫn lên, giao diện vẫn mở, và lỗi thiếu thư viện
    hiện ngay trên màn hình kèm câu lệnh cần chạy.
"""

from typing import List, Optional

from . import serializers


class ThieuThuVien(Exception):
    """Ném ra khi thiếu pandas/pytrends. routes.py đổi thành thông báo dễ hiểu."""


def _nhap(ten_package: str):
    """Nạp package công cụ, đổi lỗi thiếu thư viện thành câu tiếng Việt."""
    try:
        if ten_package == "trends":
            from trends import Settings, quet_breakout, xuat_bao_cao
            return Settings, quet_breakout, xuat_bao_cao
        from suggest import Settings, thu_thap, xuat_bao_cao
        return Settings, thu_thap, xuat_bao_cao
    except ImportError as loi:
        raise ThieuThuVien(
            f"Thiếu thư viện để chạy công cụ này ({loi}).\n\n"
            f"Mở PowerShell tại thư mục dự án và chạy:\n"
            f"python -m pip install -r requirements.txt"
        ) from loi


# =============================================================================
# GOOGLE TRENDS
# =============================================================================

def chay_trends(viec, tu_khoa: List[str], timeframe: str, geo: str,
                include_rising: bool) -> dict:
    """Quét từ khóa Breakout. Trả về dict kết quả đã sẵn sàng đổi sang JSON."""
    Settings, quet_breakout, _ = _nhap("trends")

    st = Settings(
        geo=geo,
        timeframe=timeframe,
        include_rising=include_rising,
    )

    # nen_dung: công cụ tự gọi hàm này giữa các nhóm để biết có phải dừng không.
    # Bấm Dừng giữa chừng vẫn GIỮ NGUYÊN phần kết quả đã thu được.
    df = quet_breakout(tu_khoa, st, nen_dung=viec.da_yeu_cau_dung)

    # Giữ DataFrame lại để lát nữa xuất Excel mà không phải hỏi Google lần nữa.
    viec.du_lieu_tho = {"df": df, "st": st}

    so_breakout = 0
    if len(df) and "Query Type" in df.columns:
        so_breakout = int((df["Query Type"] == "Breakout").sum())

    return {
        "bang": serializers.bang_du_lieu(df),
        "thong_ke": [
            {"ten": "Tổng số dòng", "so_luong": int(len(df))},
            {"ten": "Breakout thực sự", "so_luong": so_breakout},
            {"ten": "Từ khóa gốc đã quét", "so_luong": len(tu_khoa)},
        ],
        "co_the_xuat": bool(len(df)),
    }


# =============================================================================
# GOOGLE SUGGEST
# =============================================================================

def chay_suggest(viec, tu_khoa: List[str], nhanh: bool) -> dict:
    """Thu thập keyword làm content. Trả về dict kết quả."""
    Settings, thu_thap, _ = _nhap("suggest")

    # --quick của bản dòng lệnh = bỏ phần quét bảng chữ cái, nhanh gấp khoảng 3.
    from suggest import config as cf_suggest
    st = Settings(dung_bang_chu_cai=(cf_suggest.DUNG_BANG_CHU_CAI and not nhanh))

    df = thu_thap(tu_khoa, st, nen_dung=viec.da_yeu_cau_dung)
    viec.du_lieu_tho = {"df": df, "st": st}

    return {
        "bang": serializers.bang_du_lieu(df),
        # Số keyword theo từng nhóm ý định — đây là con số người dùng dùng để
        # quyết định viết bài gì trước, nên đưa lên đầu màn hình.
        "thong_ke": ([{"ten": "Tổng số keyword", "so_luong": int(len(df))}] +
                     serializers.dem_theo_cot(df, "Nhóm ý định")),
        "co_the_xuat": bool(len(df)),
    }


# =============================================================================
# XUẤT FILE
# =============================================================================

def xuat_file(viec, dinh_dang: str = "xlsx") -> str:
    """
    Xuất kết quả của một việc ra Excel/CSV. Trả về đường dẫn tuyệt đối.

    Dùng lại chính DataFrame đã thu, KHÔNG hỏi Google lần nữa — nhờ vậy xuất
    file bao nhiêu lần cũng được mà không tốn thêm một lượt gọi nào.
    """
    if not viec.du_lieu_tho:
        raise ValueError("Việc này chưa có dữ liệu để xuất.")

    df = viec.du_lieu_tho["df"]
    st = viec.du_lieu_tho["st"]
    if df is None or len(df) == 0:
        raise ValueError("Không có dòng nào để xuất.")

    _, _, xuat_bao_cao = _nhap(viec.loai)
    st.output_format = "csv" if dinh_dang == "csv" else "xlsx"
    return xuat_bao_cao(df, st)


# =============================================================================
# TỪ KHÓA MẶC ĐỊNH
# =============================================================================

def tu_khoa_mac_dinh(loai: str) -> List[str]:
    """
    Đọc danh sách từ khóa gốc trong config.py của công cụ.

    Giao diện điền sẵn danh sách này vào ô nhập để người dùng bấm Chạy được
    ngay, đúng như tab tkinter đang làm.
    """
    try:
        if loai == "trends":
            from trends import config as cf
        else:
            from suggest import config as cf
        return list(cf.SEED_KEYWORDS)
    except ImportError:
        # Thiếu thư viện thì trả danh sách rỗng chứ không làm sập trang chủ —
        # người dùng vẫn vào được giao diện và đọc được hướng dẫn cài đặt.
        return []


def uoc_tinh_suggest(so_tu_khoa: int, nhanh: bool) -> Optional[dict]:
    """
    Ước tính số lượt hỏi Google và số phút chạy, để hiện trước khi bấm Chạy.

    Tính bằng chính công thức của suggest/settings.py, không tự bịa con số.
    """
    try:
        from suggest import Settings, config as cf
    except ImportError:
        return None

    st = Settings(dung_bang_chu_cai=(cf.DUNG_BANG_CHU_CAI and not nhanh))
    so_bien_the = st.so_bien_the_moi_seed()
    so_luot = so_tu_khoa * so_bien_the
    so_phut = so_luot * (st.delay_min + st.delay_max) / 2 / 60

    return {
        "so_bien_the_moi_tu": so_bien_the,
        "so_luot_hoi": so_luot,
        "so_phut": round(so_phut, 1),
    }
