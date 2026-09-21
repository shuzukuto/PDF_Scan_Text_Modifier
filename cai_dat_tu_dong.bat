@echo off
chcp 65001 > nul
title Cai Dat Tu Dong 100% Cho Nguoi Khong Biet Gi

echo ======================================================================
echo     TỰ ĐỘNG CÀI ĐẶT MÔI TRƯỜNG PDF SCAN TEXT MODIFIER (1-CLICK)
echo     (Dành cho người mới - Tự động cài Python và toàn bộ thư viện)
echo ======================================================================
echo.

:: 1. Kiểm tra xem máy đã có Python chưa
where python >nul 2>&1
if %errorlevel% equ 0 (
    echo [✓] Đã tìm thấy Python trên máy tính của bạn!
    goto :INSTALL_LIBS
)

echo [-] Chưa phát hiện Python trên máy tính.
echo [*] Đang tự động tải và cài đặt Python bản chuẩn (khoảng 1 phút)...
echo.

:: 2. Thử cài bằng winget nếu có
where winget >nul 2>&1
if %errorlevel% equ 0 (
    echo [*] Đang cài đặt Python qua Windows Package Manager (winget)...
    winget install Python.Python.3.11 --silent --accept-package-agreements --accept-source-agreements
    goto :CHECK_AFTER_INSTALL
)

:: 3. Nếu không có winget, dùng PowerShell tải file cài chính thức từ python.org
echo [*] Đang tải trực tiếp gói cài đặt từ python.org qua PowerShell...
set "PY_INSTALLER=%TEMP%\python_installer.exe"
powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; (New-Object Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe', '%PY_INSTALLER%')"

if exist "%PY_INSTALLER%" (
    echo [*] Đang cài đặt Python ngầm vào máy tính (tự động bật PATH)...
    "%PY_INSTALLER%" /quiet InstallAllUsers=0 PrependPath=1 Include_pip=1
    del /f /q "%PY_INSTALLER%" >nul 2>&1
)

:CHECK_AFTER_INSTALL
:: Làm mới biến môi trường PATH
set "PATH=%LOCALAPPDATA%\Programs\Python\Python311;%LOCALAPPDATA%\Programs\Python\Python311\Scripts;%PATH%"

where python >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [LƯU Ý] Quá trình cài Python tự động cần khởi động lại cửa sổ lệnh.
    echo Bạn hãy đóng cửa sổ này lại và nhấp đúp vào 'Chay_Ung_Dung.bat' nhé!
    pause
    exit /b
)

:INSTALL_LIBS
echo.
echo ======================================================================
echo [*] Đang tự động cài đặt toàn bộ thư viện cần thiết (FastAPI, OpenCV, PyMuPDF, Pillow)...
echo ======================================================================
echo.

python -m pip install --upgrade pip
python -m pip install -r "%~dp0requirements.txt"

if %errorlevel% equ 0 (
    echo.
    echo ======================================================================
    echo [✓] CÀI ĐẶT HOÀN TẤT 100%!
    echo [*] Đang khởi động Giao diện Studio cho bạn ngay bây giờ...
    echo ======================================================================
    echo.
    timeout /t 2 >nul
    python "%~dp0run_ui.py"
) else (
    echo.
    echo [LỖI] Có lỗi xảy ra trong quá trình cài đặt thư viện.
    echo Vui lòng kiểm tra lại kết nối mạng Internet của bạn.
    pause
)
