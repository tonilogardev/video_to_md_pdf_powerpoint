# Standalone Executable & Distribution

## Index

1. [Build Instructions](#1-build-instructions)
2. [Distribution Structure](#2-distribution-structure)
3. [End-User Delivery](#3-end-user-delivery)
4. [Next steps](#4-next-steps)

---

## 1 Build Instructions

- ***Instruction***: Compile the desktop application into a standalone Windows directory distribution.
- ***File References***:
    - Build script: [build_exe.py](../build_exe.py)
    - PyInstaller specification: [build_desktop.spec](../build_desktop.spec)
    - Local static FFmpeg: [third_party/ffmpeg/ffmpeg.exe](../third_party/ffmpeg/ffmpeg.exe)
- ***Command***:
    ```powershell
    python build_exe.py
    ```
- ***Build Settings***:
    - Pure Windows GUI mode (`console=False` in [build_desktop.spec](../build_desktop.spec)).
    - Automatic bundling of PyTorch, Whisper models, FFmpeg binary, and Tkinter UI components.

[←Index](#index)

## 2 Distribution Structure

- ***Instruction***: Maintain the integrity of the generated distribution directory located at [dist/VideoToMarkdownConverter/](../dist/VideoToMarkdownConverter/).
- ***Contents***:
    - `VideoToMarkdownConverter.exe`: Main entry point executable.
    - `_internal/`: **Mandatory dependency folder** containing the embedded Python runtime, C++ DLLs (PyTorch, OpenCV, Torchvision), and bundled `ffmpeg.exe`.
- ***Rule***: Never separate `VideoToMarkdownConverter.exe` from `_internal/`. Moving the `.exe` alone will cause startup DLL errors.

[←Index](#index)

## 3 End-User Delivery

- ***Instruction***: Package and distribute the compiled application to client machines without requiring Python.
- ***Distribution Methods***:
    - **Portable ZIP**: Compress the parent folder [dist/VideoToMarkdownConverter/](../dist/VideoToMarkdownConverter/) into `VideoToMarkdownConverter_v1.0.zip`. The user extracts it and runs the executable directly.
    - **Desktop Shortcut**: Instruct users to right-click `VideoToMarkdownConverter.exe` -> **Send to -> Desktop (create shortcut)**.
    - **Setup Wizard**: Optionally package the folder using Inno Setup or NSIS to generate a single `Installer.exe` that registers shortcuts and file associations.

[←Index](#index)

## 4 Next steps

- [001_overview.md](./001_overview.md)
- [002_architecture.md](./002_architecture.md)
- [004_user_guide.md](./004_user_guide.md)
