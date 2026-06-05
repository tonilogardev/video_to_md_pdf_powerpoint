#!/bin/bash
# setup.sh - Automated Environment Setup for Linux/WSL

echo "=========================================="
echo " Setting up Video to Markdown Environment "
echo "=========================================="

# 1. Install system dependencies if 'apt' is available (Ubuntu/Debian/WSL)
if [ -x "$(command -v apt)" ]; then
    echo ">> [1/4] Installing system dependencies (ffmpeg, python3-tk, python3-venv)..."
    echo ">> (You might be prompted for your sudo password)"
    sudo apt-get update -y
    sudo apt-get install -y ffmpeg python3-tk python3-venv
else
    echo ">> [1/4] APT not found. Please ensure ffmpeg and python3-tk are installed manually."
fi

# 2. Create the virtual environment
echo ">> [2/4] Creating Python virtual environment (venv)..."
python3 -m venv venv

# 3. Activate the virtual environment
echo ">> [3/4] Activating virtual environment..."
source venv/bin/activate

# 4. Install Python requirements
echo ">> [4/4] Installing Python dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

echo "=========================================="
echo " Setup Complete! 🎉"
echo " To run the application, type:"
echo "   source venv/bin/activate"
echo "   python main.py"
echo "=========================================="
