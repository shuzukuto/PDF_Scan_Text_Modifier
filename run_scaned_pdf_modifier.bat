@echo off
title PDF Scan Text Modifier Studio
cls

echo ======================================================================
echo    PDF SCAN TEXT MODIFIER STUDIO
echo ======================================================================
echo.

:: 1. Thiet lap ten mien pdfscanmodifier neu chua co
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup_domain.ps1"

:: 2. Uu tien khoi chay ban Standalone EXE neu co
if exist "%~dp0dist\PDF_Scan_Modifier\PDF_Scan_Modifier.exe" (
    echo [*] Dang khoi dong ban doc lap Standalone EXE...
    start "" "%~dp0dist\PDF_Scan_Modifier\PDF_Scan_Modifier.exe"
    exit /b
)

if exist "%~dp0PDF_Scan_Modifier.exe" (
    echo [*] Dang khoi dong ban doc lap Standalone EXE...
    start "" "%~dp0PDF_Scan_Modifier.exe"
    exit /b
)

:: 3. Khoi chay qua moi truong Python
where python >nul 2>&1
if %errorlevel% equ 0 (
    echo [*] Dang khoi dong qua Python...
    python "%~dp0run_ui.py"
    exit /b
)

:: 4. Thong bao neu chua co Python
echo [THONG BAO] May tinh chua co Python va chua co file EXE.
echo Vui long chay file cai_dat_tu_dong.bat de tu dong cai dat.
pause
