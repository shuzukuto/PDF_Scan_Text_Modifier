@echo off
chcp 65001 > nul
title PDF Scan Text Modifier Studio
cls

echo ======================================================================
echo    PDF SCAN TEXT MODIFIER STUDIO
echo ======================================================================
echo.

:: 1. Thiet lap ten mien pdfscanmodifier neu chua co
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup_domain.ps1"

:: 2. UU TIEN 1: Khoi chay ban doc lap Standalone EXE (Khong can Python, khong can thu vien)
if exist "%~dp0dist\PDF_Scan_Modifier\PDF_Scan_Modifier.exe" (
    echo [*] Dang khoi dong ban doc lap Standalone EXE (khong can Python)...
    start "" "%~dp0dist\PDF_Scan_Modifier\PDF_Scan_Modifier.exe"
    exit /b
)

if exist "%~dp0PDF_Scan_Modifier.exe" (
    echo [*] Dang khoi dong ban doc lap Standalone EXE (khong can Python)...
    start "" "%~dp0PDF_Scan_Modifier.exe"
    exit /b
)

:: 3. UU TIEN 2: Kiem tra xem may da co Python chua
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] May tinh chua cai dat Python va chua co file EXE doc lap.
    echo [*] He thong se tu dong chuyen tiep sang Cai Dat Tu Dong 1-Click cho ban...
    echo.
    timeout /t 2 >nul
    call "%~dp0cai_dat_tu_dong.bat"
    exit /b
)

:: 4. Kiem tra xem cac thu vien can thiet da cai du chua
python -c "import uvicorn, fastapi, fitz, cv2, PIL" >nul 2>&1
if %errorlevel% neq 0 (
    echo [-] Phat hien may da co Python nhung chua cai du cac thu vien.
    echo [*] Dang tu dong cai dat cac thu vien can thiet tu requirements.txt...
    echo.
    python -m pip install -r "%~dp0requirements.txt"
    if %errorlevel% neq 0 (
        echo [LOI] Khong the cai dat thu vien. Vui long kiem tra ket noi Internet.
        pause
        exit /b
    )
    echo [v] Da cai dat xong toan bo thu vien!
    echo.
)

:: 5. Khoi chay ung dung qua Python
echo [*] Dang khoi dong Giao dien Studio...
python "%~dp0run_ui.py"
if %errorlevel% neq 0 (
    echo.
    echo [LOI] Khong the khoi chay ung dung.
    pause
)
