import os
import platform
import shutil
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path


def is_ffmpeg_on_path() -> bool:
    """Return True if ffmpeg is available on PATH."""
    from shutil import which
    return which('ffmpeg') is not None


def download_ffmpeg_windows(dest_dir: str) -> str | None:
    """Download a static ffmpeg build for Windows and extract ffmpeg.exe into dest_dir.

    Returns full path to ffmpeg.exe on success, or None on failure.
    """
    urls = [
        'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip',
        'https://github.com/GyanD/codexffmpeg/releases/download/7.1/ffmpeg-7.1-essentials_build.zip',
        'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip',
    ]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    os.makedirs(dest_dir, exist_ok=True)

    for url in urls:
        try:
            print(f"Downloading ffmpeg from {url} ...")
            with tempfile.TemporaryDirectory() as td:
                zip_path = os.path.join(td, 'ffmpeg.zip')
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=60) as resp, open(zip_path, 'wb') as out_f:
                    shutil.copyfileobj(resp, out_f)

                print("Extracting ffmpeg...")
                with zipfile.ZipFile(zip_path, 'r') as z:
                    z.extractall(td)

                # search for ffmpeg.exe under the extracted tree
                for root, dirs, files in os.walk(td):
                    if 'ffmpeg.exe' in files:
                        src = os.path.join(root, 'ffmpeg.exe')
                        dst = os.path.join(dest_dir, 'ffmpeg.exe')
                        shutil.copy2(src, dst)
                        print(f"ffmpeg installed to: {dst}")
                        return dst

        except Exception as e:
            print(f"ffmpeg download/extract from {url} failed: {e}")
            continue

    return None


def ensure_ffmpeg(dest_folder: str = None) -> str | None:
    """Ensure ffmpeg is available.

    If ffmpeg is on PATH, returns the executable path or 'ffmpeg'.
    Checks if a local copy exists in `third_party/ffmpeg` or `dest_folder`.
    On Windows, if not found, attempts to download a static build into
    `third_party/ffmpeg` inside the project and returns the full path.
    Otherwise returns None.
    """
    if is_ffmpeg_on_path():
        from shutil import which
        return which('ffmpeg') or 'ffmpeg'

    system = platform.system()
    exe_name = 'ffmpeg.exe' if system == 'Windows' else 'ffmpeg'

    # Check candidate directories (supporting normal script, PyInstaller onedir, PyInstaller onefile)
    candidates = []
    if dest_folder:
        candidates.append(Path(dest_folder))

    if getattr(sys, 'frozen', False):
        exe_dir = Path(sys.executable).parent
        candidates.append(exe_dir / 'third_party' / 'ffmpeg')
        candidates.append(exe_dir / '_internal' / 'third_party' / 'ffmpeg')
        candidates.append(exe_dir)
        if hasattr(sys, '_MEIPASS'):
            mei_dir = Path(sys._MEIPASS)
            candidates.append(mei_dir / 'third_party' / 'ffmpeg')
            candidates.append(mei_dir)
    else:
        project_root = Path(__file__).resolve().parent.parent
        candidates.append(project_root / 'third_party' / 'ffmpeg')

    # 1. Check if ffmpeg exists in any candidate location
    for folder in candidates:
        local_ffmpeg = folder / exe_name
        if local_ffmpeg.is_file():
            return str(local_ffmpeg.resolve())

    third_party = candidates[0] if candidates else (Path(__file__).resolve().parent.parent / 'third_party' / 'ffmpeg')

    # 2. If not found on Windows, attempt download
    if system == 'Windows':
        exe_path = download_ffmpeg_windows(str(third_party))
        if exe_path:
            return exe_path
        else:
            print('Automatic download failed. Please install ffmpeg manually.')
            return None

    # For non-Windows systems we don't attempt a download here
    print('ffmpeg not found and automatic installation is not implemented for this OS.')
    return None


if __name__ == '__main__':
    p = ensure_ffmpeg()
    if p:
        print('ffmpeg ready:', p)
    else:
        print('ffmpeg not available')
