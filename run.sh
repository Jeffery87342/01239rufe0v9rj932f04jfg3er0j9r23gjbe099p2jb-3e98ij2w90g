#!/bin/bash

echo "============================================================"
echo "Roblox Group Auto-Joiner"
echo "============================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed!"
    echo ""
    echo "Please install Python 3.7+ from your package manager:"
    echo "  Ubuntu/Debian: sudo apt-get install python3 python3-pip"
    echo "  macOS: brew install python3"
    exit 1
fi

echo "[INFO] Python found!"
echo ""

# Check if requests is installed
python3 -c "import requests" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[INFO] Installing required package: requests"
    pip3 install requests
    echo ""
fi

echo "[INFO] Starting Roblox Group Auto-Joiner..."
echo ""

# Run the main script
python3 main.py

read -p "Press Enter to exit..."
