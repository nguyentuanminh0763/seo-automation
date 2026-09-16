@echo off
chcp 65001 >nul
title SEO Keyword Tools - Giao dien web
cd /d "%~dp0"

rem ===========================================================================
rem  Bam dup file nay de mo giao dien WEB (chay trong trinh duyet).
rem
rem  KHAC GI Chay_giao_dien.bat?
rem    Chay_giao_dien.bat      mo cua so Windows (tkinter) - van dung binh thuong
rem    Chay_giao_dien_web.bat  mo giao dien trong trinh duyet
rem
rem  File nay dung python.exe (KHONG phai pythonw.exe) la co y: may chu web
rem  can mot cua so den de ban biet no dang chay va de tat bang Ctrl+C.
rem  Dong cua so den = tat may chu.
rem ===========================================================================

set "PY=C:\Users\PC\AppData\Local\Programs\Python\Python312\python.exe"

if exist "%PY%" goto :chay

rem --- Khong thay o duong dan mac dinh, thu tim bang launcher py ---
where py >nul 2>&1
if %errorlevel%==0 (
    py "%~dp0seo_web.py"
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
"%PY%" "%~dp0seo_web.py"

rem Neu may chu tat vi loi, giu cua so lai de ban doc duoc thong bao.
if %errorlevel% neq 0 pause
exit /b 0
