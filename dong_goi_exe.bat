@echo off
chcp 65001 > nul
title Đóng Gói Ứng Dụng EXE Độc Lập (Standalone)
cls

echo ======================================================================
echo    CÔNG CỤ TỰ ĐỘNG ĐÓNG GÓI THÀNH FILE EXE ĐỘC LẬP
echo    (Tạo thư mục dist\PDF_Scan_Modifier dùng ngay trên mọi máy Windows)
echo ======================================================================
echo.

:: 1. Kiểm tra môi trường Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [LỖI] Máy tính chưa có Python để thực hiện đóng gói.
    echo Vui lòng chạy file cai_dat_tu_dong.bat trước.
    pause
    exit /b
)

:: 2. Kiểm tra và tự động cài đặt PyInstaller nếu chưa có
where pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo [*] Chưa tìm thấy PyInstaller, đang tự động cài đặt qua pip...
    python -m pip install pyinstaller
    if %errorlevel% neq 0 (
        echo [LỖI] Cài đặt PyInstaller thất bại. Vui lòng kiểm tra mạng Internet.
        pause
        exit /b
    )
)

:: 3. Tắt tiến trình cũ nếu ứng dụng đang chạy (tránh lỗi file bị khóa)
taskkill /f /im PDF_Scan_Modifier.exe >nul 2>&1

:: 4. Tiến hành đóng gói ứng dụng qua file cấu hình PDF_Scan_Modifier.spec
echo [*] Đang đóng gói ứng dụng (quá trình này mất khoảng 30 - 60 giây)...
pyinstaller --clean PDF_Scan_Modifier.spec -y

if %errorlevel% neq 0 (
    echo.
    echo [LỖI] Quá trình đóng gói gặp sự cố. Vui lòng kiểm tra thông báo lỗi ở trên.
    pause
    exit /b
)

:: 5. Đồng bộ thư mục giao diện static vào thư mục kết quả
echo [*] Đang đồng bộ tài nguyên giao diện Web Studio...
if not exist "%~dp0dist\PDF_Scan_Modifier\static" mkdir "%~dp0dist\PDF_Scan_Modifier\static"
xcopy /E /I /Y "%~dp0static\*" "%~dp0dist\PDF_Scan_Modifier\static\" >nul 2>&1
xcopy /E /I /Y "%~dp0static\*" "%~dp0dist\PDF_Scan_Modifier\_internal\static\" >nul 2>&1

echo.
echo ======================================================================
echo [✓] ĐÓNG GÓI HOÀN TẤT THÀNH CÔNG!
echo ======================================================================
echo.
echo Thư mục kết quả nằm tại:
echo   %~dp0dist\PDF_Scan_Modifier
echo.
echo CÁCH CHIA SẺ CHO NGƯỜI KHÁC:
echo 1. Click chuột phải vào thư mục 'PDF_Scan_Modifier' -> Chọn 'Compress to ZIP file'.
echo 2. Gửi file .zip đó cho bất kỳ ai. Người nhận chỉ cần giải nén và bấm đúp
echo    vào file 'PDF_Scan_Modifier.exe' là dùng được ngay mà KHÔNG CẦN CÀI PYTHON!
echo.
echo Nhấn phím bất kỳ để mở ngay thư mục chứa file EXE...
pause >nul
start "" explorer.exe "%~dp0dist"
