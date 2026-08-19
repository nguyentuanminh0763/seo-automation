# -*- coding: utf-8 -*-
"""
Tạo kết nối tới Google Trends và các tiện ích chống bị nhận diện là bot.
"""

import random
import time

from pytrends.request import TrendReq

from .logger import lay_log
from .settings import Settings

log = lay_log()

# Danh sách User-Agent luân phiên để giảm khả năng bị Google nhận diện là bot.
_DANH_SACH_UA = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
]


def user_agent_ngau_nhien() -> str:
    """Chọn ngẫu nhiên một User-Agent trông giống trình duyệt thật."""
    return random.choice(_DANH_SACH_UA)


def tao_ket_noi(st: Settings, proxy_index: int = 0) -> TrendReq:
    """
    Khởi tạo đối tượng kết nối Google Trends cho thị trường Việt Nam.

    Tham số:
        st          : Settings của phiên chạy
        proxy_index : chỉ số proxy đang dùng; mỗi lần bị chặn sẽ tăng lên 1 để xoay vòng

    ⚠ TUYỆT ĐỐI KHÔNG truyền retries= / backoff_factor= vào TrendReq!
        pytrends 4.9.2 gọi urllib3 Retry(method_whitelist=...), nhưng urllib3 >= 2.0
        đã xóa tham số này (đổi tên thành allowed_methods), gây lỗi ngay lập tức:
            TypeError: Retry.__init__() got an unexpected keyword argument 'method_whitelist'
        Đây là lỗi đã gặp thực tế và làm hỏng toàn bộ lần chạy đầu tiên.
        Không sao cả: module fetcher.py đã có vòng retry riêng, mạnh và dễ kiểm soát hơn.
    """
    proxies = []
    if st.proxy_list:
        # Xoay vòng proxy: chia lấy dư để không bao giờ vượt quá độ dài danh sách.
        proxy_dang_dung = st.proxy_list[proxy_index % len(st.proxy_list)]
        proxies = [proxy_dang_dung]
        log.info("Đang dùng proxy: %s", proxy_dang_dung)

    return TrendReq(
        hl=st.hl,
        tz=st.tz,
        timeout=st.request_timeout,
        proxies=proxies,
        requests_args={"headers": {"User-Agent": user_agent_ngau_nhien()}},
    )


def nghi_ngau_nhien(st: Settings, ly_do: str = "") -> None:
    """Nghỉ ngẫu nhiên giữa các lượt truy vấn để tránh bị chặn IP."""
    giay = random.uniform(st.sleep_min, st.sleep_max)
    log.info("Nghỉ %.1f giây %s", giay, ly_do)
    time.sleep(giay)
