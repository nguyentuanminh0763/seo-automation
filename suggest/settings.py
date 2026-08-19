# -*- coding: utf-8 -*-
"""
Gói toàn bộ cấu hình vào một đối tượng Settings duy nhất, rồi truyền tường minh
xuống từng hàm (không dùng biến global).
"""

from dataclasses import dataclass, field
from typing import List

from . import config


@dataclass
class Settings:
    """Toàn bộ tham số cho một lần chạy thu thập keyword."""

    # --- Kết nối ---
    hl: str = config.HL
    gl: str = config.GL
    client: str = config.CLIENT
    request_timeout: int = config.REQUEST_TIMEOUT

    # --- Mở rộng từ khóa ---
    tu_moi_truoc: List[str] = field(default_factory=lambda: list(config.TU_MOI_TRUOC))
    tu_moi_sau: List[str] = field(default_factory=lambda: list(config.TU_MOI_SAU))
    dung_bang_chu_cai: bool = config.DUNG_BANG_CHU_CAI
    bang_chu_cai: str = config.BANG_CHU_CAI

    # --- Chống chặn ---
    delay_min: float = config.DELAY_MIN
    delay_max: float = config.DELAY_MAX
    max_retries: int = config.MAX_RETRIES
    cooldown_on_block: int = config.COOLDOWN_ON_BLOCK
    proxy_list: List[str] = field(default_factory=lambda: list(config.PROXY_LIST))

    # --- Lọc ---
    do_dai_toi_thieu: int = config.DO_DAI_TOI_THIEU
    tu_khoa_loai_bo: List[str] = field(
        default_factory=lambda: list(config.TU_KHOA_LOAI_BO)
    )

    # --- Đầu ra ---
    output_dir: str = config.OUTPUT_DIR
    output_prefix: str = config.OUTPUT_PREFIX
    output_format: str = "xlsx"

    @classmethod
    def tu_cli(cls, args) -> "Settings":
        """Tạo Settings từ tham số dòng lệnh. CLI ghi đè giá trị trong config.py."""
        return cls(
            # --quick = chạy nhanh, bỏ qua phần quét bảng chữ cái
            dung_bang_chu_cai=(config.DUNG_BANG_CHU_CAI and not args.quick),
            output_format=args.format,
        )

    def so_bien_the_moi_seed(self) -> int:
        """Ước tính số lượt hỏi Google cho MỖI từ gốc (để báo thời gian dự kiến)."""
        so = 1 + len(self.tu_moi_truoc) + len(self.tu_moi_sau)
        if self.dung_bang_chu_cai:
            so += len(self.bang_chu_cai)
        return so
