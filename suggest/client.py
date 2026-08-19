# -*- coding: utf-8 -*-
"""
Gọi Google Suggest (API gợi ý tự động của ô tìm kiếm Google) kèm cơ chế retry.

Đây chính là nguồn dữ liệu tạo ra những keyword dạng câu hỏi như
"cpu hàng tray là gì", "cách kiểm tra ram máy tính đơn giản".
"""

import json
import random
import time
from typing import List, Optional

import requests

from .logger import lay_log
from .settings import Settings

log = lay_log()

URL_SUGGEST = "https://suggestqueries.google.com/complete/search"

_DANH_SACH_UA = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
]

_DAU_HIEU_BI_CHAN = ("429", "too many", "quota", "rate limit", "blocked", "captcha")


class SuggestClient:
    """
    Quản lý một phiên kết nối tới Google Suggest.

    Dùng requests.Session để tái sử dụng kết nối TCP -> nhanh hơn đáng kể
    khi phải gửi cả nghìn lượt hỏi.
    """

    def __init__(self, st: Settings):
        self.st = st
        self.proxy_index = 0
        self.session = self._tao_session()

    def _tao_session(self) -> requests.Session:
        """Tạo phiên mới với User-Agent ngẫu nhiên và proxy hiện hành (nếu có)."""
        session = requests.Session()
        session.headers.update({
            "User-Agent": random.choice(_DANH_SACH_UA),
            "Accept-Language": "vi-VN,vi;q=0.9",
        })
        if self.st.proxy_list:
            proxy = self.st.proxy_list[self.proxy_index % len(self.st.proxy_list)]
            session.proxies.update({"http": proxy, "https": proxy})
            log.info("Đang dùng proxy: %s", proxy)
        return session

    def _lam_moi_session(self) -> None:
        """Bị chặn -> xoay proxy kế tiếp và tạo phiên hoàn toàn mới."""
        self.proxy_index += 1
        self.session = self._tao_session()

    def lay_goi_y(self, truy_van: str) -> Optional[List[str]]:
        """
        Hỏi Google: "gõ chuỗi này thì bạn gợi ý gì?"

        Trả về danh sách gợi ý, hoặc None nếu thất bại hoàn toàn sau các lần thử.
        """
        tham_so = {
            "client": self.st.client,
            "hl": self.st.hl,
            "gl": self.st.gl,
            "q": truy_van,
        }

        for lan_thu in range(1, self.st.max_retries + 1):
            try:
                phan_hoi = self.session.get(
                    URL_SUGGEST, params=tham_so, timeout=self.st.request_timeout
                )
                phan_hoi.raise_for_status()
                return self._doc_ket_qua(phan_hoi.text)

            except Exception as loi:  # noqa: BLE001 - không để script sập
                bi_chan = any(d in str(loi).lower() for d in _DAU_HIEU_BI_CHAN)

                if lan_thu == self.st.max_retries:
                    log.warning("Bỏ qua '%s' sau %d lần thử: %s",
                                truy_van, self.st.max_retries, str(loi)[:120])
                    return None

                if bi_chan:
                    thoi_gian_cho = self.st.cooldown_on_block * lan_thu
                    log.warning("BỊ CHẶN ở '%s' -> đổi proxy, chờ %d giây...",
                                truy_van, thoi_gian_cho)
                    self._lam_moi_session()
                    time.sleep(thoi_gian_cho)
                else:
                    time.sleep(2)

        return None

    @staticmethod
    def _doc_ket_qua(noi_dung: str) -> List[str]:
        """
        Bóc danh sách gợi ý từ chuỗi JSON Google trả về.

        Định dạng: ["truy vấn gốc", ["gợi ý 1", "gợi ý 2", ...], ...]
        Ta chỉ cần phần tử thứ 2.
        """
        du_lieu = json.loads(noi_dung)
        if len(du_lieu) < 2 or not isinstance(du_lieu[1], list):
            return []
        return [str(g).strip() for g in du_lieu[1] if str(g).strip()]


def nghi_ngan(st: Settings) -> None:
    """Nghỉ ngẫu nhiên rất ngắn giữa các lượt hỏi để tránh bị chặn IP."""
    time.sleep(random.uniform(st.delay_min, st.delay_max))
