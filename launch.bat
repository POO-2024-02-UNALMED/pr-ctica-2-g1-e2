@echo off
cd /d %~dp0
:: Check if running as administrator
openfiles >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting administrative privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:: Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
:: Run the application
echo Running the application...
python .\src\iuMain\administrador.py