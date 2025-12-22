@echo off
title Roblox Group Auto-Joiner
color 0A

echo ============================================================
echo Roblox Group Auto-Joiner
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo.
    echo Please install Python 3.7+ from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [INFO] Python found!
echo.

REM Check if requests is installed
python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing required package: requests
    pip install requests
    echo.
)

echo [INFO] Starting Roblox Group Auto-Joiner...
echo.

REM Run the main script
python main.py

pause
