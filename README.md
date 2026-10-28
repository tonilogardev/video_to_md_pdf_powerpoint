# Video to Markdown, PDF & PowerPoint Converter

A professional, standalone desktop application that converts video content (YouTube videos/playlists or local video files) into structured Markdown (`.md`) study notes, styled PDF documents (`.pdf`), and editable PowerPoint presentations (`.pptx`). It extracts audio, transcribes it with Whisper AI, and captures key visual slides.

[![Descargar para Windows (Google Drive)](https://img.shields.io/badge/Descargar%20para%20Windows-Google%20Drive-4285F4?style=for-the-badge&logo=googledrive&logoColor=white)](https://drive.google.com/file/d/1Ew-Ze7ROpfmg446ICNA-w3qNrrm7FfBY/view?usp=sharing)

---

## ✨ Features

- **Pure Graphical Experience**: 100% desktop UI with modern dialogs, clipboard auto-detection for YouTube links, and zero command prompt flashing (`CREATE_NO_WINDOW`).
- **Real-Time Progress Tracking**: Live status window showing sub-tasks (*Audio extraction*, *Whisper AI transcription*, *SSIM slide detection*, *Document generation*, and *ZIP packaging*) with timestamps and progress percentage.
- **Completion Popup**: Automatic foreground notification modal with immediate buttons to open the output folder in Windows Explorer or exit cleanly.
- **Versatile Ingestion**:
  1. **YouTube URL**: Single videos and full playlists supported via `yt-dlp`.
  2. **Local Video Files**: Select individual or multiple videos (`.mp4`, `.mkv`, `.avi`, `.mov`, `.webm`).
  3. **Local Directory**: Automatically batch-process all compatible video files found in a folder.
- **Smart Slides Detection**: Downsampled SSIM comparison extracts visual slide changes rapidly without duplicates.
- **AI Speech-to-Text**: Whisper model generates timestamped `.srt` subtitles and paragraph text.
- **Triple Export Format**:
  - **Markdown (`.md`)**: Formatted notes with embedded slide images and timestamps.
  - **PDF (`.pdf`)**: Beautifully styled, printable document with embedded slides.
  - **PowerPoint (`.pptx`)**: 16:9 widescreen presentation slides with visual frames and accompanying transcript notes.
- **Isolated Workspace & Packaging**: Output destination is selected by the user. Generates self-contained `.zip` archives and automatically purges all temporary files.

---

## 🚀 Running the Application

### Option A: Standalone Windows Executable (No Python Required)
1. **Download**: Download the standalone portable archive:
   👉 **[VideoToMarkdownConverter.zip (Google Drive)](https://drive.google.com/file/d/1Ew-Ze7ROpfmg446ICNA-w3qNrrm7FfBY/view?usp=sharing)**
2. **Extract**: Unzip the folder anywhere on your PC.
3. **Run**: Double-click `VideoToMarkdownConverter.exe` (or `dist/VideoToMarkdownConverter/VideoToMarkdownConverter.exe` if building from source).

### Option B: From Python Source
1. Install dependencies:
```bash
pip install -r requirements.txt
```
2. Run the main orchestrator:
```bash
python main.py
```

---

## 🛠️ Compiling to Windows `.exe`

To rebuild the standalone executable after code changes:
```bash
python build_exe.py
```
This bundles PyTorch, Whisper AI, FFmpeg, and the modern UI into `dist/VideoToMarkdownConverter/`.

---

## 📦 Sharing with End Users & Friends

To distribute the application to testers or friends without requiring Python installed:
- **Share the direct Google Drive link**:
  👉 **[VideoToMarkdownConverter.zip (Google Drive)](https://drive.google.com/file/d/1Ew-Ze7ROpfmg446ICNA-w3qNrrm7FfBY/view?usp=sharing)**
- **Or share your own custom build**:
  1. Locate the compiled output directory: `dist/VideoToMarkdownConverter/`
  2. Compress the entire `VideoToMarkdownConverter` folder into a `.zip` archive.
  3. Recipients extract the folder and double-click `VideoToMarkdownConverter.exe`.
  *(Note: Never separate `VideoToMarkdownConverter.exe` from its adjacent `_internal/` dependency folder).*

---

## 📚 Documentation

For in-depth architectural and development documentation, see the [documentation/](./documentation/) directory:
- [000_run_app.md](./documentation/000_run_app.md) - Quick start and installation scripts.
- [001_overview.md](./documentation/001_overview.md) - System overview, requirements, and execution guide.
- [002_architecture.md](./documentation/002_architecture.md) - Pipeline data flow and core module breakdown.
- [003_build_and_distribution.md](./documentation/003_build_and_distribution.md) - Standalone compilation and distribution guide.
- [004_user_guide.md](./documentation/004_user_guide.md) - 🇪🇸 **Guía de usuario completa**.
- [004_user_guide_en.md](./documentation/004_user_guide_en.md) - 🇬🇧 **Complete End-User Guide**.
