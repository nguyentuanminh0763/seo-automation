# -*- coding: utf-8 -*-
"""
Gọi API Google Trends với cơ chế retry - ĐẢM BẢO SCRIPT KHÔNG BAO GIỜ SẬP.

Toàn bộ logic chống chặn IP nằm gọn trong file này.
"""

import time
from typing import Dict, List, Optional

from .client import tao_ket_noi
from .logger import lay_log
from .settings import Settings

log = lay_log()

# Các dấu hiệu trong thông báo lỗi cho biết đang bị Google chặn.
_DAU_HIEU_BI_CHAN = ("429", "too many", "quota", "rate limit", "blocked")


def la_loi_bi_chan(loi: Exception) -> bool:
    """Nhận diện lỗi bị Google chặn (429 / quota / too many requests)."""
    mo_ta = str(loi).lower()
    return any(dau_hieu in mo_ta for dau_hieu in _DAU_HIEU_BI_CHAN)


class TrendsFetcher:
    """
    Quản lý một phiên kết nối Google Trends và tự phục hồi khi bị chặn.

    Dùng class thay cho biến global vì phiên kết nối cần được THAY MỚI khi bị chặn
    (đổi proxy, đổi User-Agent). Class giữ trạng thái đó gọn gàng trong chính nó.
    """

    def __init__(self, st: Settings):
        self.st = st
        self.proxy_index = 0
        self.pytrends = tao_ket_noi(st, self.proxy_index)

    def _lam_moi_ket_noi(self) -> None:
        """Bị chặn -> xoay sang proxy kế tiếp và tạo phiên kết nối hoàn toàn mới."""
        self.proxy_index += 1
        try:
            self.pytrends = tao_ket_noi(self.st, self.proxy_index)
        except Exception as loi:  # noqa: BLE001
            log.warning("Không tạo được kết nối mới: %s", loi)

    def lay_related_queries(self, nhom_tu_khoa: List[str]) -> Optional[Dict]:
        """
        Gửi payload cho 1 nhóm (tối đa 5 từ khóa) và lấy về related_queries.

        Trả về:
            dict {từ_khóa: {'top': DataFrame|None, 'rising': DataFrame|None}} nếu thành công
            None nếu đã thử hết số lần cho phép mà vẫn thất bại

        Cơ chế chống chặn:
            - Lỗi lần n  -> ngủ cooldown * n giây (60s -> 120s -> 180s) rồi thử lại
            - Bị chặn IP -> đổi proxy + tạo phiên mới trước khi thử lại
            - Hết lượt   -> ghi log ERROR rồi BỎ QUA nhóm này, chạy tiếp nhóm sau
        """
        for lan_thu in range(1, self.st.max_retries + 1):
            try:
                self.pytrends.build_payload(
                    kw_list=nhom_tu_khoa,
                    cat=self.st.category,
                    timeframe=self.st.timeframe,
                    geo=self.st.geo,
                    gprop=self.st.gprop,
                )
                ket_qua = self.pytrends.related_queries()

                # Google đôi khi trả HTTP 200 nhưng rỗng -> coi như thất bại mềm.
                if not ket_qua:
                    raise ValueError("Google trả về dữ liệu rỗng (có thể bị giới hạn mềm).")

                return ket_qua

            except Exception as loi:  # noqa: BLE001 - cố ý bắt rộng để script không sập
                bi_chan = la_loi_bi_chan(loi)
                log.warning(
                    "Lỗi lần %d/%d ở nhóm %s -> %s: %s",
                    lan_thu, self.st.max_retries, nhom_tu_khoa,
                    "BỊ CHẶN IP" if bi_chan else type(loi).__name__, loi,
                )

                if lan_thu == self.st.max_retries:
                    log.error("Bỏ qua nhóm %s sau %d lần thử.",
                              nhom_tu_khoa, self.st.max_retries)
                    return None

                if bi_chan:
                    self._lam_moi_ket_noi()

                thoi_gian_cho = self.st.cooldown_on_block * lan_thu
                log.info("Chờ %d giây rồi thử lại...", thoi_gian_cho)
                time.sleep(thoi_gian_cho)

        return None
