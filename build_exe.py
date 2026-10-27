"""
Build script to compile Video to Markdown Converter into a standalone Windows executable.
Usage:
    python build_exe.py
"""

import os
import subprocess
import sys

def main():
    print("===============================================")
    print(" Compilando VideoToMarkdownConverter a .EXE ...")
    print("===============================================")

    project_root = os.path.dirname(os.path.abspath(__file__))
    spec_file = os.path.join(project_root, "build_desktop.spec")

    if not os.path.exists(spec_file):
        print(f"Error: No se encontró el archivo spec: {spec_file}")
        sys.exit(1)

    # Ensure third_party/ffmpeg/ffmpeg.exe exists
    ffmpeg_exe = os.path.join(project_root, "third_party", "ffmpeg", "ffmpeg.exe")
    if not os.path.exists(ffmpeg_exe):
        print(f"Aviso: ffmpeg.exe no se encontró en {ffmpeg_exe}. Verificando instalación...")
        sys.path.append(project_root)
        from src.ffmpeg_installer import ensure_ffmpeg
        ensure_ffmpeg()

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--clean",
        spec_file
    ]

    print("Ejecutando comando:")
    print(" ".join(cmd))
    print("\nEste proceso puede tardar unos minutos mientras empaqueta PyTorch y Whisper...")
    ret = subprocess.call(cmd, cwd=project_root)

    if ret == 0:
        dist_dir = os.path.join(project_root, "dist", "VideoToMarkdownConverter")
        exe_path = os.path.join(dist_dir, "VideoToMarkdownConverter.exe")
        print("\n===============================================")
        print(" ¡COMPILACIÓN COMPLETADA CON ÉXITO!")
        print(f" Carpeta de distribución: {dist_dir}")
        print(f" Ejecutable principal: {exe_path}")
        print("===============================================")
    else:
        print(f"\nLa compilación falló con código de salida: {ret}")
        sys.exit(ret)

if __name__ == "__main__":
    main()
