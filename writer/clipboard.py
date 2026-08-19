# -*- coding: utf-8 -*-
"""
Đặt bài viết lên clipboard KÈM ĐỊNH DẠNG, để dán thẳng vào WordPress.

VẤN ĐỀ CẦN GIẢI:
    Khi bạn copy từ ChatGPT, clipboard Windows giữ hai bản cùng lúc:
        Bản chữ thường : "Cách kiểm tra RAM"
        Bản có định dạng: "<h2>Cách kiểm tra RAM</h2>"   <- WordPress đọc bản này
    Nhờ vậy dán vào WordPress ăn đúng tiêu đề H2.

    Tkinter chỉ đặt được bản chữ thường. Nếu dùng cách thông thường, dán vào
    WordPress sẽ ra một cục chữ trơn mất hết định dạng.

CÁCH GIẢI:
    Gọi thẳng Windows API để ghi cả hai bản, trong đó bản định dạng dùng
    "HTML Format" — đúng chuẩn Microsoft mà trình duyệt và Word đều dùng.

    Nếu vì lý do gì đó không ghi được, luôn còn đường lui: lưu file .html
    rồi mở bằng trình duyệt, Ctrl+A Ctrl+C (xem formatter.boc_trang_html).
"""

import ctypes
import sys
from ctypes import wintypes
from typing import Optional

CF_UNICODETEXT = 13

# GMEM_MOVEABLE | GMEM_ZEROINIT.
# Bắt buộc có ZEROINIT: nếu không, Windows cấp vùng nhớ còn nguyên dữ liệu cũ
# của chương trình khác, và phần dư sau nội dung của ta trở thành rác đuôi.
# Đã gặp thật khi test: đọc lại clipboard thấy "</html> aGl[..." — ký tự lạ.
GMEM_MOVEABLE = 0x0042

# Khung bao bắt buộc của chuẩn "HTML Format". Các con số StartHTML/EndHTML...
# là VỊ TRÍ BYTE trong chính chuỗi này, nên phải tính sau khi dựng xong khung.
_KHUNG = (
    "Version:0.9\r\n"
    "StartHTML:{start_html:010d}\r\n"
    "EndHTML:{end_html:010d}\r\n"
    "StartFragment:{start_frag:010d}\r\n"
    "EndFragment:{end_frag:010d}\r\n"
    "<html><body>\r\n"
    "<!--StartFragment-->{noi_dung}<!--EndFragment-->\r\n"
    "</body></html>"
)


class LoiClipboard(Exception):
    """Không ghi được lên clipboard."""


def ho_tro_dinh_dang() -> bool:
    """Chỉ Windows mới ghi được clipboard có định dạng bằng cách này."""
    return sys.platform == "win32"


def chep_kem_dinh_dang(than_html: str, ban_chu_thuong: str) -> None:
    """
    Ghi cả hai bản lên clipboard.

    Tham số:
        than_html      : phần HTML, vd "<h2>Tiêu đề</h2><p>Nội dung</p>"
        ban_chu_thuong : bản chữ trơn, dành cho chỗ chỉ nhận text (Notepad...)

    Ném LoiClipboard nếu thất bại — giao diện bắt và gợi ý dùng đường lui.
    """
    if not ho_tro_dinh_dang():
        raise LoiClipboard("Chỉ hỗ trợ trên Windows.")

    du_lieu_html = _dung_chuoi_html(than_html)

    user32 = ctypes.WinDLL("user32", use_last_error=True)
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    _khai_bao_kieu(user32, kernel32)

    ma_dinh_dang = user32.RegisterClipboardFormatW("HTML Format")
    if not ma_dinh_dang:
        raise LoiClipboard("Windows không cấp được định dạng HTML cho clipboard.")

    if not user32.OpenClipboard(None):
        raise LoiClipboard(
            "Không mở được clipboard.\n"
            "Thường do phần mềm khác đang giữ nó (trình quản lý clipboard, "
            "Remote Desktop...). Thử lại sau vài giây."
        )

    try:
        user32.EmptyClipboard()
        # Bản có định dạng: mã hóa UTF-8 theo đúng chuẩn HTML Format
        _dat_du_lieu(user32, kernel32, ma_dinh_dang, du_lieu_html.encode("utf-8"))
        # Bản chữ thường: Windows yêu cầu UTF-16, kết thúc bằng ký tự rỗng
        _dat_du_lieu(user32, kernel32, CF_UNICODETEXT,
                     ban_chu_thuong.encode("utf-16-le") + b"\x00\x00")
    finally:
        user32.CloseClipboard()


# =============================================================================
# CHI TIẾT KỸ THUẬT
# =============================================================================

def _dung_chuoi_html(than_html: str) -> str:
    """
    Dựng chuỗi đúng chuẩn "HTML Format", tính sẵn các vị trí byte.

    Làm hai lượt: lượt đầu điền số 0 để biết độ dài khung, lượt sau điền
    số thật. Phải đếm theo BYTE của bản UTF-8, không phải theo ký tự —
    tiếng Việt có dấu chiếm 2-3 byte mỗi chữ.
    """
    def dung(start_html, end_html, start_frag, end_frag) -> str:
        return _KHUNG.format(
            start_html=start_html, end_html=end_html,
            start_frag=start_frag, end_frag=end_frag,
            noi_dung=than_html,
        )

    tam = dung(0, 0, 0, 0)

    def vi_tri_byte(chuoi: str, moc: str, sau_moc: bool = False) -> int:
        chi_so = chuoi.index(moc)
        if sau_moc:
            chi_so += len(moc)
        return len(chuoi[:chi_so].encode("utf-8"))

    start_html = vi_tri_byte(tam, "<html>")
    start_frag = vi_tri_byte(tam, "<!--StartFragment-->", sau_moc=True)
    end_frag = vi_tri_byte(tam, "<!--EndFragment-->")
    end_html = len(tam.encode("utf-8"))

    return dung(start_html, end_html, start_frag, end_frag)


def _khai_bao_kieu(user32, kernel32) -> None:
    """
    Khai báo kiểu dữ liệu cho các hàm Windows.

    BẮT BUỘC trên Windows 64-bit: nếu không khai báo, ctypes mặc định coi
    giá trị trả về là số nguyên 32-bit, làm con trỏ bộ nhớ bị cắt mất nửa
    trên và chương trình sập.
    """
    user32.OpenClipboard.argtypes = [wintypes.HWND]
    user32.OpenClipboard.restype = wintypes.BOOL
    user32.EmptyClipboard.restype = wintypes.BOOL
    user32.CloseClipboard.restype = wintypes.BOOL
    user32.RegisterClipboardFormatW.argtypes = [wintypes.LPCWSTR]
    user32.RegisterClipboardFormatW.restype = wintypes.UINT
    user32.SetClipboardData.argtypes = [wintypes.UINT, wintypes.HANDLE]
    user32.SetClipboardData.restype = wintypes.HANDLE

    kernel32.GlobalAlloc.argtypes = [wintypes.UINT, ctypes.c_size_t]
    kernel32.GlobalAlloc.restype = wintypes.HGLOBAL
    kernel32.GlobalLock.argtypes = [wintypes.HGLOBAL]
    kernel32.GlobalLock.restype = ctypes.c_void_p
    kernel32.GlobalUnlock.argtypes = [wintypes.HGLOBAL]
    kernel32.GlobalUnlock.restype = wintypes.BOOL
    kernel32.GlobalFree.argtypes = [wintypes.HGLOBAL]
    kernel32.GlobalFree.restype = wintypes.HGLOBAL


def _dat_du_lieu(user32, kernel32, ma_dinh_dang: int, du_lieu: bytes) -> None:
    """
    Cấp bộ nhớ toàn cục, chép dữ liệu vào, giao cho clipboard.

    Sau khi SetClipboardData thành công, Windows SỞ HỮU vùng nhớ đó —
    không được giải phóng. Chỉ giải phóng khi thất bại.
    """
    bo_nho = kernel32.GlobalAlloc(GMEM_MOVEABLE, len(du_lieu) + 2)
    if not bo_nho:
        raise LoiClipboard("Không cấp được bộ nhớ cho clipboard.")

    con_tro = kernel32.GlobalLock(bo_nho)
    if not con_tro:
        kernel32.GlobalFree(bo_nho)
        raise LoiClipboard("Không khóa được vùng nhớ clipboard.")

    try:
        ctypes.memmove(con_tro, du_lieu, len(du_lieu))
    finally:
        kernel32.GlobalUnlock(bo_nho)

    if not user32.SetClipboardData(ma_dinh_dang, bo_nho):
        kernel32.GlobalFree(bo_nho)
        raise LoiClipboard("Windows từ chối nhận dữ liệu clipboard.")


def chep_chu_thuong(widget, noi_dung: str) -> None:
    """
    Đường lui: chép chữ trơn bằng tkinter. Luôn chạy được, nhưng dán vào
    WordPress sẽ mất định dạng.
    """
    widget.clipboard_clear()
    widget.clipboard_append(noi_dung)
    widget.update()
