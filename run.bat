@echo off
title EXIF Metadata Editor
color 0A

echo ================================================
echo     EXIF Metadata Editor - PNG Image Tool
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from python.org
    pause
    exit /b 1
)

echo [+] Python detected
echo.

REM Check if ExifTool is installed
exiftool -ver >nul 2>&1
if errorlevel 1 (
    echo [WARNING] ExifTool not detected
    echo.
    echo Please install ExifTool from: https://exiftool.org/
    echo.
    echo Installation steps:
    echo 1. Download ExifTool for Windows
    echo 2. Extract the .zip file
    echo 3. Rename 'exiftool(-k).exe' to 'exiftool.exe'
    echo 4. Add to system PATH or place in this folder
    echo.
    echo The application will start, but won't work without ExifTool.
    echo.
    pause
) else (
    echo [+] ExifTool detected
    echo.
)

echo [*] Starting EXIF Metadata Editor...
echo.

REM Run the application
python main.py

if errorlevel 1 (
    echo.
    echo [ERROR] Application crashed or exited with error
    pause
)
