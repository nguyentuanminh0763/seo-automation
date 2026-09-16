# -*- coding: utf-8 -*-
"""
Máy chủ web: dựng ứng dụng FastAPI, phục vụ giao diện React đã build.

AN TOÀN — ĐỌC TRƯỚC KHI SỬA:
    API này đọc/ghi file trên máy bạn và chạy được công cụ thu thập. Ba chốt
    dưới đây phải giữ nguyên:

    1. Chỉ nghe ở 127.0.0.1. Đổi sang "0.0.0.0" là mở cửa cho cả mạng LAN.
    2. Chỉ nhận yêu cầu có Host là localhost. Không có chốt này, một trang web
       bất kỳ có thể trỏ tên miền của họ về 127.0.0.1 rồi gọi API của bạn
       (kiểu tấn công gọi là DNS rebinding).
    3. Không bật CORS cho nguồn lạ. Chỉ khi chạy `npm run dev` mới mở đúng
       cổng 5173 của máy mình.
"""

import os
import socket
import webbrowser

from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from . import config, routes


def tao_ung_dung(thu_muc_goc: str, dev: bool = False) -> FastAPI:
    """Dựng ứng dụng FastAPI hoàn chỉnh."""
    app = FastAPI(
        title="SEO Keyword Tools — Đô Lar",
        description="Giao diện web cho hai công cụ thu thập từ khóa.",
        version="1.0.0",
        # Tài liệu API tự sinh, mở bằng http://127.0.0.1:8765/docs
        docs_url="/docs",
        redoc_url=None,
    )

    # Chốt 2: chặn Host lạ.
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=list(config.HOST_HOP_LE))

    # Chốt 3: chỉ mở CORS khi lập trình giao diện bằng `npm run dev`.
    if dev:
        from fastapi.middleware.cors import CORSMiddleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[config.NGUON_DEV],
            allow_methods=["*"],
            allow_headers=["*"],
        )

    routes.dat_thu_muc_goc(thu_muc_goc)
    app.include_router(routes.router)

    _gan_giao_dien(app, thu_muc_goc)
    return app


def _gan_giao_dien(app: FastAPI, thu_muc_goc: str) -> None:
    """
    Phục vụ giao diện React đã build.

    Chưa build thì hiện trang hướng dẫn thay vì lỗi 404 trống trơn — người
    không lập trình nhìn 404 sẽ không biết phải làm gì.
    """
    thu_muc_web = os.path.join(thu_muc_goc, config.THU_MUC_WEB)

    if os.path.isdir(thu_muc_web):
        # html=True: vào "/" thì tự trả index.html.
        # Gắn ở cuối cùng để không nuốt mất các đường dẫn /api/.
        app.mount("/", StaticFiles(directory=thu_muc_web, html=True), name="web")
        return

    @app.get("/", response_class=HTMLResponse)
    def chua_build():
        return f"""<!doctype html>
<html lang="vi"><head><meta charset="utf-8">
<title>Chưa có giao diện</title>
<style>
 body{{font-family:system-ui,Segoe UI,sans-serif;max-width:680px;margin:60px auto;
      padding:0 20px;line-height:1.7;color:#1a2330}}
 code{{background:#eef1f6;padding:2px 7px;border-radius:5px}}
 pre{{background:#0f172a;color:#e2e8f0;padding:16px;border-radius:10px;overflow:auto}}
</style></head><body>
<h1>Chưa có file giao diện</h1>
<p>Máy chủ đã chạy tốt, nhưng không tìm thấy thư mục:</p>
<p><code>{thu_muc_web}</code></p>
<p>Thư mục này chứa giao diện React đã build. Dựng lại bằng hai lệnh:</p>
<pre>cd web
npm install
npm run build</pre>
<p>Phần API vẫn dùng được bình thường:
<a href="/docs">xem tài liệu API</a>.</p>
</body></html>"""


# =============================================================================

def _cong_con_trong(cong: int) -> int:
    """
    Tìm cổng còn trống, bắt đầu từ cổng mặc định.

    Mở hai lần giao diện, hoặc một chương trình khác đang giữ cổng 8765, thì
    uvicorn sẽ chết ngay lúc khởi động với một dòng lỗi tiếng Anh khó hiểu.
    Thà nhảy sang cổng kế tiếp và báo rõ.
    """
    for buoc in range(20):
        thu = cong + buoc
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                s.bind((config.DIA_CHI, thu))
                return thu
            except OSError:
                continue
    return cong


def chay(thu_muc_goc: str, cong: int = config.CONG,
         dev: bool = False, mo_trinh_duyet: bool = True) -> None:
    """Khởi động máy chủ. Hàm này chỉ trả về khi người dùng tắt máy chủ."""
    import uvicorn

    cong = _cong_con_trong(cong)
    dia_chi = f"http://{config.DIA_CHI}:{cong}"

    print("=" * 62)
    print(" GIAO DIỆN WEB — SEO KEYWORD TOOLS (Đô Lar)")
    print("=" * 62)
    print(f" Mở trình duyệt tại:  {dia_chi}")
    print(f" Tài liệu API:        {dia_chi}/docs")
    print(" Tắt máy chủ:         bấm Ctrl + C trong cửa sổ này")
    print("=" * 62)

    if mo_trinh_duyet:
        # Mở sau một nhịp để uvicorn kịp lắng nghe, tránh trình duyệt vào sớm
        # và nhận "không kết nối được".
        import threading
        threading.Timer(1.2, lambda: webbrowser.open(dia_chi)).start()

    uvicorn.run(
        tao_ung_dung(thu_muc_goc, dev=dev),
        host=config.DIA_CHI,
        port=cong,
        log_level="warning",   # log của công cụ đã hiện trên giao diện rồi
    )
