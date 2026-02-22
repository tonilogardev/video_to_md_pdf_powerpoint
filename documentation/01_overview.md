# Video to Markdown & PDF Converter

## Index

1. [Overview](#1-overview)
2. [Prerequisites](#2-prerequisites)
3. [Setup](#3-setup)
4. [Execution](#4-execution)
5. [Next steps](#5-next-steps)

---

## 1 Overview

- ***Instruction***: Use this tool to process video files (local or YouTube) into structured Markdown and PDF notes.
- ***Features***:
    - Extracts audio using `ffmpeg`.
    - Transcribes speech using `openai-whisper`.
    - Captures unique slides using SSIM frame comparison.
    - Generates `.md` and `.pdf` documents.
    - Packages all output into a `.zip` file.
- ***Visuals***:
    ![Output Example](./img/output_example.png)

[←Index](#index)

## 2 Prerequisites

- ***Instruction***: Ensure system-level dependencies are installed.
- ***Requirements***: 
    - `python 3.9+`
    - `ffmpeg` (Required for video/audio processing).

[←Index](#index)

## 3 Setup

- ***Instruction***: Install Python dependencies from the root directory.
- ***File References***:
    - View [requirements.txt](../requirements.txt)
- ***Command***:
    ```bash
    pip install -r requirements.txt
    ```

[←Index](#index)

## 4 Execution

- ***Instruction***: Run the main Desktop orchestrator.
- ***File References***:
    - Execute [main.py](../main.py)
- ***Command***:
    ```bash
    python main.py
    ```
- ***Menu Options***:
    1. YouTube URL
    2. Local File(s)
    3. Local Directory

[←Index](#index)

## 5 Next steps

- [02_architecture.md](./02_architecture.md)
