#!/bin/bash

# EXIF Metadata Editor Launcher for Linux/macOS

echo "================================================"
echo "    EXIF Metadata Editor - PNG Image Tool"
echo "================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

echo "[+] Python detected: $(python3 --version)"
echo ""

# Check if ExifTool is installed
if ! command -v exiftool &> /dev/null; then
    echo "[WARNING] ExifTool not detected"
    echo ""
    echo "Please install ExifTool:"
    echo ""
    echo "Ubuntu/Debian:"
    echo "  sudo apt-get install libimage-exiftool-perl"
    echo ""
    echo "macOS (with Homebrew):"
    echo "  brew install exiftool"
    echo ""
    echo "The application will start, but won't work without ExifTool."
    echo ""
    read -p "Press Enter to continue..."
else
    echo "[+] ExifTool detected: $(exiftool -ver)"
    echo ""
fi

echo "[*] Starting EXIF Metadata Editor..."
echo ""

# Run the application
python3 main.py

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Application crashed or exited with error"
    read -p "Press Enter to exit..."
fi
