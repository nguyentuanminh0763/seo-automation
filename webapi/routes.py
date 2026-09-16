# -*- coding: utf-8 -*-
"""
Khai báo các đường dẫn API. THÊM TÍNH NĂNG THÌ SỬA FILE NÀY.

Mọi đường dẫn đều bắt đầu bằng /api/ để không lẫn với file giao diện.

DANH SÁCH ĐƯỜNG DẪN:

    GET  /api/trang-thai        Thông tin khởi động: từ khóa mặc định, tùy chọn
    POST /api/trends/chay       Bắt đầu quét Google Trends
    POST /api/suggest/chay      Bắt đầu thu thập Google Suggest
    POST /api/suggest/uoc-tinh  Tính trước số lượt hỏi và số phút
    GET  /api/viec              Danh sách việc trong phiên này
    GET  /api/viec/{id}         Ảnh chụp trạng thái một việc
    GET  /api/viec/{id}/dong    Kênh SSE nghe tiến trình chạy dần
    POST /api/viec/{id}/dung    Bấm Dừng giữa chừng
    POST /api/viec/{id}/xuat    Xuất Excel/CSV từ kết quả đã thu
    GET  /api/tai-ve/{ten_file} Tải file kết quả về máy
"""

import json
import os
import queue
from typing import List, Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel, Field

from . import config, jobs, runners

router = APIRouter(prefix="/api")

# Thư mục gốc dự án — nơi chứa output/. Đặt lúc khởi động trong server.py.
THU_MUC_GOC = os.path.abspath(".")


def dat_thu_muc_goc(duong_dan: str) -> None:
    global THU_MUC_GOC
    THU_MUC_GOC = os.path.abspath(duong_dan)


# =============================================================================
# KIỂU DỮ LIỆU GỬI LÊN
# =============================================================================
# Pydantic tự kiểm tra giúp: gửi thiếu trường hoặc sai kiểu thì FastAPI trả lỗi
# 422 kèm mô tả, không để dữ liệu hỏng chui xuống tới công cụ thu thập.

class YeuCauTrends(BaseModel):
    tu_khoa: List[str] = Field(..., min_length=1)
    timeframe: str = "today 1-m"
    geo: str = "VN"
    include_rising: bool = False


class YeuCauSuggest(BaseModel):
    tu_khoa: List[str] = Field(..., min_length=1)
    nhanh: bool = False


class YeuCauUocTinh(BaseModel):
    so_tu_khoa: int = Field(..., ge=0)
    nhanh: bool = False


class YeuCauXuat(BaseModel):
    dinh_dang: str = "xlsx"


# =============================================================================
# KHỞI ĐỘNG
# =============================================================================

@router.get("/trang-thai")
def trang_thai():
    """Giao diện gọi đúng một lần lúc mở trang, để điền sẵn mọi thứ."""
    tu_khoa_trends = runners.tu_khoa_mac_dinh("trends")
    return {
        "san_sang": bool(tu_khoa_trends),
        "thieu_thu_vien": not tu_khoa_trends,
        "trends": {
            "tu_khoa_mac_dinh": tu_khoa_trends,
            "khung_thoi_gian": [{"ma": m, "ten": t}
                                for m, t in config.KHUNG_THOI_GIAN],
            "khu_vuc": [{"ma": m, "ten": t} for m, t in config.KHU_VUC],
        },
        "suggest": {
            "tu_khoa_mac_dinh": runners.tu_khoa_mac_dinh("suggest"),
        },
        "viec_dang_chay": (lambda v: v.tom_tat() if v else None)(
            jobs.kho.dang_ban("trends")),
    }


# =============================================================================
# BẮT ĐẦU CHẠY
# =============================================================================

def _tao_viec(loai: str, mo_ta: str, cong_viec):
    """Tạo việc, đổi lỗi 'đang bận' thành mã HTTP 409 cho giao diện hiểu."""
    try:
        viec = jobs.kho.tao_va_chay(loai, mo_ta, cong_viec)
    except jobs.DangBan as loi:
        dang_chay = jobs.kho.lay(str(loi))
        raise HTTPException(
            status_code=409,
            detail={
                "thong_diep": (
                    "Đang có một lượt thu thập chạy dở. Chờ nó xong hoặc bấm "
                    "Dừng đã.\n\nHai công cụ cố ý không chạy song song được: "
                    "gấp đôi số lần hỏi Google từ cùng một địa chỉ IP là cách "
                    "nhanh nhất để bị chặn IP vài giờ."
                ),
                "viec_dang_chay": dang_chay.tom_tat() if dang_chay else None,
            },
        ) from loi
    return {"id": viec.id, "trang_thai": viec.trang_thai}


@router.post("/trends/chay")
def chay_trends(yc: YeuCauTrends):
    mo_ta = f"{len(yc.tu_khoa)} từ khóa · {yc.timeframe} · {yc.geo}"
    return _tao_viec("trends", mo_ta, lambda viec: runners.chay_trends(
        viec, yc.tu_khoa, yc.timeframe, yc.geo, yc.include_rising))


@router.post("/suggest/chay")
def chay_suggest(yc: YeuCauSuggest):
    mo_ta = f"{len(yc.tu_khoa)} từ khóa gốc" + (" · chế độ nhanh" if yc.nhanh else "")
    return _tao_viec("suggest", mo_ta, lambda viec: runners.chay_suggest(
        viec, yc.tu_khoa, yc.nhanh))


@router.post("/suggest/uoc-tinh")
def uoc_tinh(yc: YeuCauUocTinh):
    """Tính trước số lượt hỏi Google và số phút, hiện ngay khi người dùng gõ."""
    ket_qua = runners.uoc_tinh_suggest(yc.so_tu_khoa, yc.nhanh)
    if ket_qua is None:
        raise HTTPException(status_code=503, detail={
            "thong_diep": "Chưa cài thư viện nên chưa tính được. "
                          "Chạy: python -m pip install -r requirements.txt"})
    return ket_qua


# =============================================================================
# THEO DÕI VIỆC
# =============================================================================

def _lay_viec(ma: str) -> jobs.Viec:
    viec = jobs.kho.lay(ma)
    if viec is None:
        raise HTTPException(status_code=404, detail={
            "thong_diep": "Không tìm thấy lượt chạy này. Nhiều khả năng máy chủ "
                          "đã khởi động lại — kết quả chỉ nằm trong bộ nhớ."})
    return viec


@router.get("/viec")
def danh_sach_viec():
    return {"cac_viec": jobs.kho.danh_sach()}


@router.get("/viec/{ma}")
def mot_viec(ma: str):
    return _lay_viec(ma).tom_tat()


@router.post("/viec/{ma}/dung")
def dung_viec(ma: str):
    """
    Bấm Dừng. Công cụ thoát ở điểm kiểm tra gần nhất và GIỮ NGUYÊN kết quả
    đã thu được — không mất phần đã chạy.
    """
    viec = _lay_viec(ma)
    viec.yeu_cau_dung()
    viec.ghi_log("WARNING", "Đã nhận lệnh Dừng. Đang dừng ở bước an toàn gần nhất...")
    return {"id": viec.id, "da_nhan": True}


@router.get("/viec/{ma}/dong")
def dong_su_kien(ma: str):
    """
    Kênh SSE: trình duyệt mở một kết nối và nghe tiến trình chạy dần.

    VÌ SAO KHÔNG TRẢ KẾT QUẢ NGAY TRONG YÊU CẦU CHẠY?
        Một lần chạy Suggest mất khoảng 13 phút. Trình duyệt, proxy và mọi thiết
        bị trên đường đi đều tự cắt kết nối trước đó rất lâu. Nên yêu cầu chạy
        chỉ trả về mã số, còn tiến trình đi qua kênh riêng này.

    Hàm khai bằng `def` chứ không phải `async def` là CỐ Ý: nó đọc hàng đợi bằng
    lệnh chờ (blocking). FastAPI sẽ đẩy hàm đồng bộ sang luồng riêng, nên việc
    chờ ở đây không làm đứng cả máy chủ. Viết thành `async def` thì lệnh chờ sẽ
    khóa chết vòng lặp sự kiện và mọi yêu cầu khác treo theo.
    """
    viec = _lay_viec(ma)

    def sinh_su_kien():
        hang_doi: "queue.Queue[dict]" = queue.Queue(maxsize=5000)
        phat_lai = viec.dang_ky_nghe(hang_doi)
        try:
            # Phát lại những gì đã xảy ra, để tab mở muộn hoặc vừa tải lại
            # trang vẫn thấy đủ tiến trình thay vì một ô log trống.
            for su_kien in phat_lai:
                yield _goi_sse(su_kien)

            if viec.trang_thai in (jobs.XONG, jobs.DA_DUNG, jobs.LOI):
                yield _goi_sse({"loai": "ket_thuc"})
                return

            while True:
                try:
                    su_kien = hang_doi.get(timeout=config.NHIP_GIU_KET_NOI)
                except queue.Empty:
                    # Lúc Suggest đang nghỉ chống chặn, hàng phút không có log
                    # nào. Gửi một dòng chú thích để kết nối không bị cắt.
                    yield ": van-con-song\n\n"
                    continue

                yield _goi_sse(su_kien)
                if su_kien.get("loai") in ("xong", "loi"):
                    yield _goi_sse({"loai": "ket_thuc"})
                    return
        finally:
            # Người dùng đóng tab -> phải gỡ hàng đợi ra, không thì việc đang
            # chạy cứ nhồi sự kiện vào một hàng đợi không ai đọc cho tới khi đầy.
            viec.huy_nghe(hang_doi)

    return StreamingResponse(
        sinh_su_kien(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            # Tắt bộ đệm của proxy. Có bộ đệm thì log dồn cục rồi mới hiện,
            # đúng thứ cần tránh — cả điểm mạnh của màn này là thấy tiến trình.
            "X-Accel-Buffering": "no",
        },
    )


def _goi_sse(su_kien: dict) -> str:
    """Đóng gói một sự kiện theo đúng định dạng SSE."""
    return f"data: {json.dumps(su_kien, ensure_ascii=False)}\n\n"


# =============================================================================
# XUẤT VÀ TẢI FILE
# =============================================================================

@router.post("/viec/{ma}/xuat")
def xuat(ma: str, yc: YeuCauXuat):
    viec = _lay_viec(ma)
    try:
        duong_dan = runners.xuat_file(viec, yc.dinh_dang)
    except (ValueError, runners.ThieuThuVien) as loi:
        raise HTTPException(status_code=400,
                            detail={"thong_diep": str(loi)}) from loi

    ten_file = os.path.basename(duong_dan)
    viec.ghi_log("INFO", f"Đã xuất file: {duong_dan}")
    return {
        "ten_file": ten_file,
        "duong_dan": duong_dan,
        "lien_ket_tai": f"/api/tai-ve/{ten_file}",
    }


@router.get("/tai-ve/{ten_file}")
def tai_ve(ten_file: str):
    """
    Tải file kết quả về máy.

    CHẶN ĐƯỜNG DẪN LẠ: chỉ file nằm trong output/ mới tải được. Không có chốt
    này thì một tên file kiểu "../../.env" sẽ lôi được API key ra ngoài.
    """
    thu_muc = os.path.realpath(os.path.join(THU_MUC_GOC, config.THU_MUC_OUTPUT))
    duong_dan = os.path.realpath(os.path.join(thu_muc, ten_file))

    if os.path.commonpath([thu_muc, duong_dan]) != thu_muc:
        raise HTTPException(status_code=403, detail={
            "thong_diep": "Chỉ tải được file trong thư mục output."})
    if not os.path.isfile(duong_dan):
        raise HTTPException(status_code=404, detail={
            "thong_diep": f"Không tìm thấy file {ten_file}."})

    return FileResponse(duong_dan, filename=os.path.basename(duong_dan))
