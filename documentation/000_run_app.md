# Setup Environment

## Index

1. [Automated Setup](#1-automated-setup)
2. [Manual Setup (Optional)](#2-manual-setup-optional)
3. [Run Application](#3-run-application)
4. [Next steps](#4-next-steps)

---

## 1 Automated Setup

- ***Instruction***: Run the automated setup script for your OS. This automatically installs system dependencies (`ffmpeg`, `python3-tk`), creates the virtual environment, and installs all Python packages.
- ***Windows***: `setup.bat`
- ***Linux / WSL***: `bash setup.sh`
- ***File References***:
    - Review [setup.bat](../setup.bat)
    - Review [setup.sh](../setup.sh)

[←Index](#index)

## 2 Manual Setup (Optional)

- ***Instruction***: If you prefer to install everything manually step by step, use these commands instead.
- ***Windows***: 
  ```powershell
  winget install ffmpeg
  python -m venv venv
  .\venv\Scripts\activate
  pip install -r requirements.txt
  ```
- ***Linux / WSL***: 
  ```bash
  sudo apt install ffmpeg python3-tk python3-venv
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```
- ***File References***:
    - Review [requirements.txt](../requirements.txt)

[←Index](#index)

## 3 Run Application

- ***Instruction***: Ensure your environment is activated, then run the main orchestrator script.
- ***Windows***:
  ```powershell
  .\venv\Scripts\activate
  python main.py
  ```
- ***Linux / WSL***:
  ```bash
  source venv/bin/activate
  python main.py
  ```
- ***File References***:
    - Execute [main.py](../main.py)

[←Index](#index)

## 4 Next steps

- [001_overview.md](./001_overview.md)
