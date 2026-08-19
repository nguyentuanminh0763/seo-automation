# -*- coding: utf-8 -*-
"""
Gói cấu hình từ file .env thành một đối tượng Settings.
"""

import os
from dataclasses import dataclass
from typing import Optional

from . import config
from .env import doc_env


class ThieuCauHinh(Exception):
    """Ném ra khi thiếu API key hoặc cấu hình sai. Giao diện bắt và hiện hướng dẫn."""


@dataclass
class Settings:
    """Toàn bộ tham số cho một lần viết bài."""

    nha_cung_cap: str = config.NHA_CUNG_CAP_MAC_DINH
    api_key: str = ""
    model: str = ""
    max_tokens: int = config.MAX_TOKENS_MAC_DINH
    timeout: int = config.TIMEOUT_MAC_DINH
    thu_muc_goc: str = "."

    @classmethod
    def tu_env(cls, thu_muc_goc: str) -> "Settings":
        """
        Đọc .env và dựng Settings. Ném ThieuCauHinh nếu thiếu key.

        Biến môi trường thật của hệ điều hành được ưu tiên hơn file .env,
        để sau này chạy tự động trên máy chủ vẫn dùng được.
        """
        env = doc_env(thu_muc_goc)

        def lay(khoa: str, mac_dinh: str = "") -> str:
            return (os.environ.get(khoa) or env.get(khoa) or mac_dinh).strip()

        nha_cung_cap = lay("NHA_CUNG_CAP", config.NHA_CUNG_CAP_MAC_DINH).lower()

        if nha_cung_cap == "gemini":
            api_key = lay("GEMINI_API_KEY")
            model = lay("GEMINI_MODEL", config.GEMINI_MODEL_MAC_DINH)
            ten_khoa = "GEMINI_API_KEY"
            noi_lay = "https://aistudio.google.com (miễn phí)"
        elif nha_cung_cap == "claude":
            api_key = lay("ANTHROPIC_API_KEY")
            model = lay("CLAUDE_MODEL", config.CLAUDE_MODEL_MAC_DINH)
            ten_khoa = "ANTHROPIC_API_KEY"
            noi_lay = "https://console.anthropic.com (trả phí)"
        else:
            raise ThieuCauHinh(
                f"NHA_CUNG_CAP trong file .env đang là '{nha_cung_cap}'.\n"
                f"Chỉ nhận 'gemini' hoặc 'claude'."
            )

        if not api_key:
            raise ThieuCauHinh(
                f"Chưa điền {ten_khoa} trong file .env\n\n"
                f"Lấy key tại: {noi_lay}\n"
                f"Rồi mở file .env bằng Notepad và dán vào dòng {ten_khoa}="
            )

        return cls(
            nha_cung_cap=nha_cung_cap,
            api_key=api_key,
            model=model,
            max_tokens=int(lay("MAX_TOKENS", str(config.MAX_TOKENS_MAC_DINH)) or
                           config.MAX_TOKENS_MAC_DINH),
            timeout=int(lay("TIMEOUT", str(config.TIMEOUT_MAC_DINH)) or
                        config.TIMEOUT_MAC_DINH),
            thu_muc_goc=thu_muc_goc,
        )

    def mo_ta(self) -> str:
        """Chuỗi ngắn hiện trên giao diện cho biết đang dùng AI nào."""
        ten = "Gemini (miễn phí)" if self.nha_cung_cap == "gemini" else "Claude (trả phí)"
        return f"{ten} · {self.model}"

    def bang_gia(self) -> Optional[dict]:
        """Lấy đơn giá của model hiện tại, None nếu không có trong bảng."""
        if self.nha_cung_cap == "gemini":
            return config.BANG_GIA["gemini"]
        return config.BANG_GIA.get(self.model)
