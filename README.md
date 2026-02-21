# Video to Markdown Converter

A professional tool to convert video content (YouTube or Local) into structured Markdown notes with keyframes and subtitles.

## Features
- **Hybrid UI**: Auto-detects Google Colab (Cloud) vs Local Machine.
- **Forma Agnostic**: Converts any video format to MP4 automatically.
- **Smart Slides**: Uses SSIM to deduplicate frames and capture only unique content.
- **Whisper AI**: State-of-the-art speech-to-text transcription.

## Installation

```bash
pip install -r requirements.txt
# Ensure ffmpeg is installed on your system!
```

## Usage

**Option 1: Jupyter Notebook (Recommended)**
Open `notebooks/run_converter.ipynb` and run the cells.

**Option 2: Google Colab**
Upload the `video_to_md` folder to your Drive/Colab and run the notebook.
