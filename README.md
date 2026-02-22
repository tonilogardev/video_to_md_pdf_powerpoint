# Video to Markdown & PDF Converter

A professional, standalone Python desktop tool that converts video content (YouTube or Local files) into structured Markdown (`.md`) and nicely formatted PDF (`.pdf`) documents. It extracts audio, transcribes it using AI, and intelligently captures key visual slides.

## ✨ Features
- **Desktop First**: Pure Python tool run from the terminal (`main.py`) using native pop-ups (`tkinter`) for easy file and directory selection.
- **Versatile Input**:
  1.  **YouTube URL**: Supports both single videos and full Playlists.
  2.  **Local Files**: Select one or multiple video files from your hard drive.
  3.  **Local Directory**: Choose a folder to automatically process all compatible videos inside.
- **Format Agnostic**: Automatically converts any non-MP4 input (`.avi`, `.mkv`, `.mov`, `.webm`) to standard `.mp4` using `ffmpeg`.
- **Intelligent Visuals ("Smart Slides")**: Uses Structural Similarity Index (SSIM) to deduplicate frames, capturing only when the slide/scene actually changes.
- **AI Transcription**: Uses state-of-the-art speech-to-text (`openai-whisper`) to create precise `.srt` subtitles and document text.
- **Dual Export**: Generates both standard Markdown (`.md`) and a rendered PDF (`.pdf`) with embedded images for immediate reading and sharing.
- **Clean Packaging**: Bundles all generated assets (Video, MP3, SRT, MD, PDF, and Frames) into a single, neat `.zip` package, automatically cleaning up temporary files.

## ⚙️ Requirements & Installation

1. **System Dependency**: You must have `ffmpeg` installed on your system.
   - Linux: `sudo apt install ffmpeg`
   - Windows: Install via `winget` or download from the official site.
   - macOS: `brew install ffmpeg`

2. **Python Dependencies**:
```bash
pip install -r requirements.txt
```
*(Make sure this includes: `yt-dlp`, `openai-whisper`, `opencv-python`, `scikit-image`, `markdown-pdf`)*

## 🚀 Usage

Simply run the main orchestrator script from your terminal:

```bash
python main.py
```

You will see an interactive menu:
```text
========================================
   Video to Markdown Converter (Desktop)
========================================

Select Input Method:
1. YouTube URL
2. Local File(s)
3. Local Directory
Enter 1, 2, or 3: 
```

Follow the on-screen instructions or the popup dialogs to select your media. Grab a coffee while the AI transcribes and processes your video into a neat Zip package!



- [01_overview.md](./documentation/01_overview.md)
