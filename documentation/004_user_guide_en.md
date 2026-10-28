# User Guide: Video to Markdown & Presentation Suite

> **Language / Idioma:** [ 🇬🇧 English ](./004_user_guide_en.md) | [ 🇪🇸 Español ](./004_user_guide.md)

## Index

1. [Starting the Application](#1-starting-the-application)
2. [Option 1: Process YouTube URL](#2-option-1-process-youtube-url)
3. [Option 2: Process Local Video File(s)](#3-option-2-process-local-video-files)
4. [Option 3: Process Full Video Folder](#4-option-3-process-full-video-folder)
5. [Destination Folder Selection & Execution](#5-destination-folder-selection--execution)
6. [Output Package Contents](#6-output-package-contents)
7. [Next steps](#7-next-steps)

---

## 1 Starting the Application

- ***Instruction***: Launch the desktop suite from the compiled executable or via Python.
    - Executable: Run [dist/VideoToMarkdownConverter/VideoToMarkdownConverter.exe](../dist/VideoToMarkdownConverter/VideoToMarkdownConverter.exe).
    - Script: Run `python main.py` from the project root.
- ***Built-in Help***: Click the bottom **📖 Guía de uso** button in the main menu window to open this guide at any time.
- ***Visuals***:
    ![Main Menu](./img/main_menu.png)
- ***File References***:
    - Entry point: [main.py](../main.py)
    - Graphical selector: [src/ui_selector.py](../src/ui_selector.py)

[←Index](#index)

---

## 2 Option 1: Process YouTube URL

- ***Instruction***: Click **1. URL de YouTube (Vídeo individual o Lista de reproducción)**.
- ***Steps***:
    1. Paste or type the video or playlist link into the text box.
    2. Right-click to access the context menu (**Paste**, **Copy**, **Cut**, **Select All**).
    3. Click **Continuar** (or press the `Enter` key).
    4. If the link belongs to a playlist, choose whether to download the entire playlist or only the selected video.
- ***Visuals***:
    ![YouTube URL Dialog](./img/youtube_dialog.png)
- ***File References***:
    - yt-dlp download manager: [src/input_handler.py](../src/input_handler.py)

[←Index](#index)

---

## 3 Option 2: Process Local Video File(s)

- ***Instruction***: Click **2. Seleccionar Archivo(s) de Vídeo Local(es)**.
- ***Steps***:
    1. Navigate to your video files in Windows Explorer.
    2. Select one or multiple videos simultaneously by holding `Ctrl` or `Shift`.
    3. Supported formats: `.mp4`, `.mkv`, `.avi`, `.mov`, `.webm`.
    4. Click **Open**.
- ***File References***:
    - FFmpeg format normalizer: [src/converter.py](../src/converter.py)

[←Index](#index)

---

## 4 Option 3: Process Full Video Folder

- ***Instruction***: Click **3. Seleccionar Carpeta con Vídeos (Lotes)**.
- ***Steps***:
    1. Select the folder containing your video recordings or course lectures.
    2. Click **Select Folder**.
    3. The application scans the folder recursively and batch-processes all supported videos sequentially.
- ***File References***:
    - Input scanner: [src/input_handler.py](../src/input_handler.py)

[←Index](#index)

---

## 5 Destination Folder Selection & Execution

- ***Instruction***: Choose the output folder and monitor conversion progress.
- ***Steps***:
    1. Select the destination folder for the generated `.zip` packages.
    2. The **Progress Window** runs the sequential pipeline in the background:
       - MP3 audio extraction.
       - Synchronized Whisper AI transcription.
       - Computer vision slide detection (SSIM).
       - Markdown notes, PDF compilation, and PowerPoint generation.
       - ZIP packaging and temporary file cleanup.
    3. When finished, the floating modal **¡Tarea Completada!** appears with buttons to **📂 Abrir Carpeta de Resultados** (Open Output Folder) or **Salir de la Aplicación** (Exit).
- ***Visuals***:
    ![Completion Modal](./img/completion_modal.png)
- ***File References***:
    - Progress and modal dialogs: [src/progress_window.py](../src/progress_window.py)

[←Index](#index)

---

## 6 Output Package Contents

- ***Instruction***: Unzip the generated `.zip` archive to access your study materials.
- ***Visuals***:
    ![Package Structure](./img/package_contents.png)
- ***Generated Files***:
    - `frames/`: Folder containing all extracted slide screenshots.
    - `001.md`: Formatted Markdown notes with embedded slide frames.
    - `001.pdf`: Styled standalone PDF document with embedded images.
    - `001.pptx`: 16:9 widescreen PowerPoint deck (slides on left, transcript notes on right).
    - `001.mp3`: Extracted audio track from the original video.
    - `001.srt`: Subtitle file with synchronized timestamps.
    - `001.mp4`: Standard normalized video file.
- ***File References***:
    - ZIP packager: [src/packager.py](../src/packager.py)
    - Markdown generator: [src/markdown_gen.py](../src/markdown_gen.py)
    - PDF generator: [src/pdf_gen.py](../src/pdf_gen.py)
    - PowerPoint generator: [src/ppt_gen.py](../src/ppt_gen.py)

[←Index](#index)

---

## 7 Next steps

- [001_overview.md](./001_overview.md)
- [002_architecture.md](./002_architecture.md)
- [003_build_and_distribution.md](./003_build_and_distribution.md)
- [README.md](../README.md)
