# -*- coding: utf-8 -*-
"""
Điều phối quy trình quét: chia nhóm -> gọi API -> lọc -> gom kết quả.
"""

from typing import Dict, Iterator, List

import pandas as pd

from .client import nghi_ngau_nhien
from .fetcher import TrendsFetcher
from .filters import loc_breakout
from .logger import lay_log
from .settings import Settings

log = lay_log()


def chia_nhom(danh_sach: List[str], kich_thuoc: int) -> Iterator[List[str]]:
    """
    Chia danh sách từ khóa hạt giống thành các nhóm nhỏ (tối đa 5 từ/nhóm).

    Đây là RÀNG BUỘC BẮT BUỘC của Google Trends: mỗi payload so sánh tối đa 5 keyword.
    Ví dụ: 20 từ khóa -> 4 nhóm, mỗi nhóm 5 từ.
    """
    for i in range(0, len(danh_sach), kich_thuoc):
        yield danh_sach[i:i + kich_thuoc]


def lam_sach_seed(danh_sach: List[str]) -> List[str]:
    """Bỏ khoảng trắng thừa, bỏ dòng rỗng, bỏ trùng lặp - nhưng GIỮ NGUYÊN thứ tự gốc."""
    da_thay = set()
    ket_qua = []
    for tu_khoa in danh_sach:
        tu_khoa = (tu_khoa or "").strip()
        khoa_so_sanh = tu_khoa.lower()
        if tu_khoa and khoa_so_sanh not in da_thay:
            da_thay.add(khoa_so_sanh)
            ket_qua.append(tu_khoa)
    return ket_qua


def quet_breakout(seed_keywords: List[str],
                  st: Settings,
                  nen_dung=None) -> pd.DataFrame:
    """
    Duyệt toàn bộ từ khóa hạt giống theo từng nhóm, gom kết quả về một DataFrame.

    Tham số:
        nen_dung : hàm không tham số trả về True khi người dùng bấm Dừng.
                   Dùng cho giao diện đồ họa. Để None khi chạy dòng lệnh.
                   Được kiểm tra giữa các nhóm, nên có thể mất vài giây mới dừng hẳn.

    Trả về DataFrame rỗng nếu không tìm thấy gì (không ném lỗi).
    """
    seed_keywords = lam_sach_seed(seed_keywords)
    if not seed_keywords:
        log.error("Danh sách từ khóa hạt giống đang rỗng.")
        return pd.DataFrame()

    cac_nhom = list(chia_nhom(seed_keywords, st.batch_size))
    log.info("Tổng %d từ khóa hạt giống -> chia thành %d nhóm (tối đa %d từ/nhóm).",
             len(seed_keywords), len(cac_nhom), st.batch_size)
    log.info("Khung thời gian: %s | Khu vực: %s | Chế độ: %s",
             st.timeframe, st.geo, st.mo_ta_che_do())

    fetcher = TrendsFetcher(st)
    tat_ca_dong: List[Dict] = []
    nhom_that_bai: List[List[str]] = []

    for thu_tu, nhom in enumerate(cac_nhom, start=1):
        # Người dùng bấm Dừng trên giao diện -> thoát sớm nhưng VẪN GIỮ kết quả đã thu.
        if nen_dung is not None and nen_dung():
            log.warning("Đã dừng theo yêu cầu. Giữ lại %d kết quả thu được.", len(tat_ca_dong))
            break

        log.info("--- [Nhóm %d/%d] %s", thu_tu, len(cac_nhom), nhom)

        du_lieu = fetcher.lay_related_queries(nhom)

        if du_lieu is None:
            nhom_that_bai.append(nhom)
        else:
            tat_ca_dong.extend(_xu_ly_ket_qua_nhom(du_lieu, nhom, st))

        # Nghỉ giữa các nhóm, trừ nhóm cuối cùng.
        if thu_tu < len(cac_nhom):
            nghi_ngau_nhien(st, "trước nhóm tiếp theo...")

    if nhom_that_bai:
        log.warning("Có %d nhóm không lấy được dữ liệu: %s",
                    len(nhom_that_bai), nhom_that_bai)

    return _hoan_thien_dataframe(tat_ca_dong)


def _xu_ly_ket_qua_nhom(du_lieu: Dict, nhom: List[str], st: Settings) -> List[Dict]:
    """Bóc tách kết quả API của một nhóm thành các dòng báo cáo."""
    cac_dong: List[Dict] = []

    for seed in nhom:
        # pytrends trả dict có key đúng bằng từ khóa đã gửi; giá trị có thể là None.
        bang = du_lieu.get(seed) or {}
        bang_rising = bang.get("rising") if isinstance(bang, dict) else None

        dong_moi = loc_breakout(seed, bang_rising, st)
        cac_dong.extend(dong_moi)

        so_breakout = sum(1 for d in dong_moi if d["Query Type"] == "Breakout")
        log.info("    • %-22s -> %2d kết quả (%d Breakout)",
                 seed, len(dong_moi), so_breakout)

    return cac_dong


def _hoan_thien_dataframe(cac_dong: List[Dict]) -> pd.DataFrame:
    """Gom về DataFrame, bỏ trùng và sắp xếp ưu tiên Breakout lên đầu."""
    if not cac_dong:
        return pd.DataFrame()

    df = pd.DataFrame(cac_dong)

    # Một từ khóa đột biến có thể xuất hiện ở nhiều seed khác nhau -> bỏ trùng.
    df = df.drop_duplicates(subset=["Seed Keyword", "Breakout Keyword"], keep="first")

    # Sắp xếp: Breakout lên đầu, sau đó theo seed rồi tới thứ hạng.
    df["_uu_tien"] = (df["Query Type"] != "Breakout").astype(int)
    df = df.sort_values(by=["_uu_tien", "Seed Keyword", "Rank"]).drop(columns=["_uu_tien"])

    return df.reset_index(drop=True)
