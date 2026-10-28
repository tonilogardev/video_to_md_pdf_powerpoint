# System Architecture

## Index

1. [Data Flow](#1-data-flow)
2. [Core Modules](#2-core-modules)
3. [Next steps](#3-next-steps)

---

## 1 Data Flow

- ***Instruction***: The processing pipeline executes sequentially in a background thread orchestrated by [main.py](../main.py) and tracked by [src/progress_window.py](../src/progress_window.py).
- ***Stages***:
    1. **Input & Destination Selection**: Capture media source and output folder via [src/ui_selector.py](../src/ui_selector.py).
    2. **Ingestion**: Download YouTube stream via `yt-dlp` or collect local paths in [src/input_handler.py](../src/input_handler.py).
    3. **Normalization**: Transcode non-MP4 formats to standard H.264 MP4 via [src/converter.py](../src/converter.py).
    4. **Audio Extraction**: Extract mono MP3 using silent background FFmpeg in [src/audio_extractor.py](../src/audio_extractor.py).
    5. **AI Transcription**: Generate text and timestamped `.srt` subtitles using OpenAI Whisper in [src/transcriber.py](../src/transcriber.py).
    6. **Smart Frame Extraction**: Detect visual slide transitions on downsampled thumbnails using SSIM in [src/frame_extractor.py](../src/frame_extractor.py).
    7. **Document Generation**:
        - Render Markdown notes with embedded images via [src/markdown_gen.py](../src/markdown_gen.py).
        - Compile standalone PDF document via [src/pdf_gen.py](../src/pdf_gen.py).
        - Create 16:9 PowerPoint presentation via [src/ppt_gen.py](../src/ppt_gen.py).
    8. **Packaging & Cleanup**: Bundle assets into `.zip` in destination folder and purge temporary workspace via [src/packager.py](../src/packager.py).
    9. **Completion Notification**: Display floating modal dialog with quick action buttons in [src/progress_window.py](../src/progress_window.py).
- ***Visuals***:
    ![Architecture Pipeline](./img/architecture_pipeline.png)

[←Index](#index)

## 2 Core Modules

- ***Instruction***: Review individual modules located in the [src/](../src/) directory.
- ***File References***:
    - User interface dialogs: [src/ui_selector.py](../src/ui_selector.py)
    - Live progress & completion modal: [src/progress_window.py](../src/progress_window.py)
    - Video ingestion & YouTube downloader: [src/input_handler.py](../src/input_handler.py)
    - Video normalization: [src/converter.py](../src/converter.py)
    - Audio extraction: [src/audio_extractor.py](../src/audio_extractor.py)
    - Whisper AI transcription: [src/transcriber.py](../src/transcriber.py)
    - SSIM slide detection: [src/frame_extractor.py](../src/frame_extractor.py)
    - Markdown note generation: [src/markdown_gen.py](../src/markdown_gen.py)
    - PDF document rendering: [src/pdf_gen.py](../src/pdf_gen.py)
    - PowerPoint presentation creation: [src/ppt_gen.py](../src/ppt_gen.py)
    - ZIP packaging & isolation: [src/packager.py](../src/packager.py)
    - FFmpeg auto-discovery & install: [src/ffmpeg_installer.py](../src/ffmpeg_installer.py)
    - Main orchestrator: [main.py](../main.py)

[←Index](#index)

## 3 Next steps

- [001_overview.md](./001_overview.md)
- [003_build_and_distribution.md](./003_build_and_distribution.md)
- [004_user_guide.md](./004_user_guide.md)
