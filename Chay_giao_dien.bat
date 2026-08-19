@echo off
chcp 65001 >nul
title SEO Keyword Tools
cd /d "%~dp0"

rem ===========================================================================
rem  Bam dup file nay de mo giao dien SEO Keyword Tools.
rem
rem  Python tren may nay KHONG nam trong PATH nen phai goi duong dan day du.
rem  Neu ban cai lai Python o cho khac, sua dong PY= ben duoi cho dung.
rem ===========================================================================

set "PY=C:\Users\PC\AppData\Local\Programs\Python\Python312\pythonw.exe"

if exist "%PY%" goto :chay

rem --- Khong thay o duong dan mac dinh, thu tim bang launcher py ---
where py >nul 2>&1
if %errorlevel%==0 (
    start "" pyw "%~dp0seo_gui.pyw"
    exit /b 0
)

rem --- Van khong thay: bao loi ro rang thay vi nhay tat ---
echo.
echo  ============================================================
echo   KHONG TIM THAY PYTHON
echo  ============================================================
echo.
echo   Da tim o: %PY%
echo.
echo   Cach xu ly:
echo     1. Cai Python:  winget install --id Python.Python.3.12 -e
echo     2. Hoac sua dong "set PY=" trong file .bat nay cho dung
echo        duong dan python tren may ban.
echo.
pause
exit /b 1

:chay
start "" "%PY%" "%~dp0seo_gui.pyw"
exit /b 0
