# -*- coding: utf-8 -*-
"""
Gói toàn bộ cấu hình vào MỘT đối tượng Settings duy nhất.

Vì sao cần file này?
    Bản cũ dùng biến global rồi sửa bằng lệnh `global TIMEFRAME, GEO` - rất dễ sinh bug
    khi nhiều module cùng đọc/ghi. Nay mọi tham số được đóng gói 1 lần ở main(),
    rồi truyền tường minh xuống từng hàm. Nhìn vào chữ ký hàm là biết nó cần gì.
"""

from dataclasses import dataclass, field
from typing import List, Tuple

from . import config


@dataclass
class Settings:
    """Toàn bộ tham số cho một lần chạy quét."""

    # --- Kết nối ---
    hl: str = config.HL
    tz: int = config.TZ
    geo: str = config.GEO
    timeframe: str = config.TIMEFRAME
    category: int = config.CATEGORY
    gprop: str = config.GPROP
    request_timeout: Tuple[int, int] = config.REQUEST_TIMEOUT

    # --- Chống chặn IP ---
    batch_size: int = config.BATCH_SIZE
    sleep_min: float = config.SLEEP_MIN
    sleep_max: float = config.SLEEP_MAX
    max_retries: int = config.MAX_RETRIES
    cooldown_on_block: int = config.COOLDOWN_ON_BLOCK
    proxy_list: List[str] = field(default_factory=lambda: list(config.PROXY_LIST))

    # --- Lọc ---
    breakout_threshold: int = config.BREAKOUT_THRESHOLD
    rising_threshold: int = config.RISING_THRESHOLD
    include_rising: bool = False   # True = lấy cả từ khóa Rising, không chỉ Breakout

    # --- Đầu ra ---
    output_dir: str = config.OUTPUT_DIR
    output_prefix: str = config.OUTPUT_PREFIX
    output_format: str = "xlsx"    # 'xlsx' hoặc 'csv'

    @classmethod
    def tu_cli(cls, args) -> "Settings":
        """Tạo Settings từ tham số dòng lệnh (argparse). CLI ghi đè lên config.py."""
        return cls(
            geo=args.geo,
            timeframe=args.timeframe,
            include_rising=args.include_rising,
            output_format=args.format,
        )

    def mo_ta_che_do(self) -> str:
        """Chuỗi mô tả ngắn để in ra log đầu phiên chạy."""
        if self.include_rising:
            return f"Breakout + Rising (>= {self.rising_threshold}%)"
        return "CHỈ Breakout"
