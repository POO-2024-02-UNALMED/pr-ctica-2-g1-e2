@echo off
cd /d %~dp0

:: Check if running as administrator
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting administrative privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:: Install dependencies
echo Installing dependencies...
pip install -r requirements.txt || python -m pip install -r requirements.txt || py -m pip install -r requirements.txt || python3 -m pip install -r requirements.txt || py3 -m pip install -r requirements.txt

:: Run the application
echo Running the application...
python .\src\iuMain\administrador.py || py .\src\iuMain\administrador.py || python3 .\src\iuMain\administrador.py || py3 .\src\iuMain\administrador.py