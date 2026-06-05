@echo off
echo ==========================================
echo  Setting up Video to Markdown Environment 
echo ==========================================

echo ^>^> [1/3] Creating Python virtual environment (venv)...
python -m venv venv

echo ^>^> [2/3] Activating virtual environment...
call venv\Scripts\activate.bat

echo ^>^> [3/3] Installing Python dependencies from requirements.txt...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo ==========================================
echo  Setup Complete! 🎉
echo  Make sure you have 'ffmpeg' installed on your system.
echo  To run the application, type:
echo    venv\Scripts\activate
echo    python main.py
echo ==========================================
pause
