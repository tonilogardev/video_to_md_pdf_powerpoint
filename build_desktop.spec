# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Critical hidden imports for AI, image, and document processing
hidden_imports = [
    'whisper',
    'tiktoken',
    'tiktoken_ext',
    'tiktoken_ext.openai_public',
    'scipy',
    'scipy.special',
    'skimage',
    'skimage.metrics',
    'skimage.metrics.simple_metrics',
    'markdown_pdf',
    'pptx',
    'cv2',
    'PIL',
    'torch',
    'unittest',
    'yt_dlp',
    'src',
    'src.ffmpeg_installer',
    'src.input_handler',
    'src.converter',
    'src.audio_extractor',
    'src.transcriber',
    'src.frame_extractor',
    'src.markdown_gen',
    'src.pdf_gen',
    'src.ppt_gen',
    'src.packager',
    'src.ui_selector',
    'src.progress_window',
    'src.ui_utils',
]

# Collect submodules dynamically for libraries that use dynamic loading
hidden_imports += collect_submodules('whisper')
hidden_imports += collect_submodules('tiktoken')
hidden_imports += collect_submodules('tiktoken_ext')
hidden_imports += collect_submodules('skimage')

datas = []

# Bundle application documentation and images
doc_dir = os.path.abspath('documentation')
if os.path.exists(doc_dir):
    datas.append((doc_dir, 'documentation'))

# Bundle the local static FFmpeg binary
ffmpeg_path = os.path.abspath('third_party/ffmpeg/ffmpeg.exe')
if os.path.exists(ffmpeg_path):
    datas.append((ffmpeg_path, 'third_party/ffmpeg'))

# Collect static assets (e.g. whisper assets like mel_filters.npz)
datas += collect_data_files('whisper')
try:
    datas += collect_data_files('tiktoken')
except Exception:
    pass

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['IPython', 'notebook'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='VideoToMarkdownConverter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False, # Pure Desktop GUI without background terminal window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='documentation/img/logo.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='VideoToMarkdownConverter',
)
