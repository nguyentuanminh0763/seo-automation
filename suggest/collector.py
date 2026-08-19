# -*- coding: utf-8 -*-
"""
Điều phối quy trình: từ gốc -> sinh biến thể -> hỏi Google -> lọc -> phân loại -> gom bảng.
"""

from datetime import datetime
from typing import Dict, List

import pandas as pd

from .classifier import la_keyword_rac, phan_loai, uu_tien_content
from .client import SuggestClient, nghi_ngan
from .expander import sinh_bien_the
from .logger import lay_log
from .settings import Settings

log = lay_log()


def thu_thap(seed_keywords: List[str],
             st: Settings,
             nen_dung=None) -> pd.DataFrame:
    """
    Chạy toàn bộ quy trình thu thập cho danh sách từ khóa gốc.

    Tham số:
        nen_dung : hàm không tham số trả về True khi người dùng bấm Dừng.
                   Dùng cho giao diện đồ họa. Để None khi chạy dòng lệnh.

    Trả về DataFrame rỗng nếu không thu được gì (không ném lỗi).
    """
    seed_keywords = _lam_sach(seed_keywords)
    if not seed_keywords:
        log.error("Danh sách từ khóa gốc đang rỗng.")
        return pd.DataFrame()

    so_luot = len(seed_keywords) * st.so_bien_the_moi_seed()
    uoc_tinh_phut = so_luot * (st.delay_min + st.delay_max) / 2 / 60

    log.info("Có %d từ khóa gốc × %d biến thể = khoảng %d lượt hỏi Google.",
             len(seed_keywords), st.so_bien_the_moi_seed(), so_luot)
    log.info("Thời gian dự kiến: khoảng %.0f phút. Cứ để chạy, đừng tắt.", uoc_tinh_phut)

    client = SuggestClient(st)
    thoi_diem = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Dùng dict để bỏ trùng ngay khi thu thập: 1 keyword chỉ xuất hiện 1 lần
    # dù nhiều từ gốc khác nhau cùng moi ra nó.
    kho_keyword: Dict[str, Dict] = {}

    for thu_tu, seed in enumerate(seed_keywords, start=1):
        # Người dùng bấm Dừng trên giao diện -> thoát sớm nhưng VẪN GIỮ kết quả đã thu.
        if nen_dung is not None and nen_dung():
            log.warning("Đã dừng theo yêu cầu. Giữ lại %d keyword thu được.", len(kho_keyword))
            break

        so_moi = _thu_thap_mot_seed(seed, client, st, kho_keyword, thoi_diem, nen_dung)
        log.info("[%2d/%2d] %-22s -> +%d keyword mới (tổng %d)",
                 thu_tu, len(seed_keywords), seed, so_moi, len(kho_keyword))

    return _hoan_thien_dataframe(list(kho_keyword.values()))


def _thu_thap_mot_seed(seed: str,
                       client: SuggestClient,
                       st: Settings,
                       kho_keyword: Dict[str, Dict],
                       thoi_diem: str,
                       nen_dung=None) -> int:
    """Xử lý một từ khóa gốc. Trả về số keyword MỚI thu được."""
    so_moi = 0

    for truy_van in sinh_bien_the(seed, st):
        # Kiểm tra ở đây nữa vì mỗi seed mất ~30 giây, chờ hết seed mới dừng là quá lâu.
        if nen_dung is not None and nen_dung():
            break

        goi_y = client.lay_goi_y(truy_van)
        nghi_ngan(st)

        if not goi_y:
            continue

        for keyword in goi_y:
            khoa = keyword.lower().strip()

            if khoa in kho_keyword or la_keyword_rac(keyword, st):
                continue

            nhom, loai_bai = phan_loai(keyword)
            kho_keyword[khoa] = {
                "Keyword chính": keyword,
                "Nhóm ý định": nhom,
                "Loại bài đề xuất": loai_bai,
                "Từ khóa gốc": seed,
                "Số từ": len(keyword.split()),
                "Truy vấn nguồn": truy_van,
                "Timestamp": thoi_diem,
            }
            so_moi += 1

    return so_moi


def _lam_sach(danh_sach: List[str]) -> List[str]:
    """Bỏ khoảng trắng thừa, dòng rỗng và trùng lặp - giữ nguyên thứ tự gốc."""
    da_thay = set()
    ket_qua = []
    for tu_khoa in danh_sach:
        tu_khoa = (tu_khoa or "").strip()
        khoa = tu_khoa.lower()
        if tu_khoa and khoa not in da_thay:
            da_thay.add(khoa)
            ket_qua.append(tu_khoa)
    return ket_qua


def _hoan_thien_dataframe(cac_dong: List[Dict]) -> pd.DataFrame:
    """Gom về DataFrame và sắp xếp theo thứ tự ưu tiên làm content."""
    if not cac_dong:
        return pd.DataFrame()

    df = pd.DataFrame(cac_dong)

    # Sắp xếp: nhóm dễ lên top lên trước, trong mỗi nhóm thì keyword dài hơn
    # (cụ thể hơn, ít cạnh tranh hơn) lên trước.
    df["_uu_tien"] = df["Nhóm ý định"].map(uu_tien_content)
    df = df.sort_values(by=["_uu_tien", "Số từ", "Keyword chính"],
                        ascending=[True, False, True])
    df = df.drop(columns=["_uu_tien"])

    return df.reset_index(drop=True)
