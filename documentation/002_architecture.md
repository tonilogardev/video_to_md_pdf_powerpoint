# System Architecture

## Index

1. [Data Flow](#1-data-flow)
2. [Core Modules](#2-core-modules)
3. [Next steps](#3-next-steps)

---

## 1 Data Flow

- ***Instruction***: The pipeline executes sequentially through the modules located in `src/`.
- ***Stages***:
    1. Input Selection (UI/CLI).
    2. Download/Validation.
    3. Transcode to standard MP4 (if necessary).
    4. Audio Extraction -> AI Transcription.
    5. Frame Extraction (SSIM diffing).
    6. Markdown & PDF Generation.
    7. Zip Packaging & Cleanup.
- ***Visuals***:
    ![Architecture Pipeline](./img/architecture_pipeline.png)

[←Index](#index)

## 2 Core Modules

- ***Instruction***: Review the logic within individual source files.
- ***File References***:
    - Manage inputs: [src/input_handler.py](../src/input_handler.py)
    - Handle native UI dialogs: [src/ui_selector.py](../src/ui_selector.py)
    - Convert non-mp4 files: [src/converter.py](../src/converter.py)
    - Extract mp3 audio: [src/audio_extractor.py](../src/audio_extractor.py)
    - Whisper AI Speech-to-Text: [src/transcriber.py](../src/transcriber.py)
    - Deduplicate frames via SSIM: [src/frame_extractor.py](../src/frame_extractor.py)
    - Assemble `.md` file: [src/markdown_gen.py](../src/markdown_gen.py)
    - Render `.pdf` file: [src/pdf_gen.py](../src/pdf_gen.py)
    - Zip and cleanup: [src/packager.py](../src/packager.py)

[←Index](#index)

## 3 Next steps

- [01_overview.md](./01_overview.md)
