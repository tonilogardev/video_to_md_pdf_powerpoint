import os
import sys
import tkinter as tk
from PIL import Image, ImageTk

def get_asset_path(filename: str) -> str:
    """
    Locates an asset file across development and PyInstaller bundled environments.
    """
    possible_roots = []
    if getattr(sys, 'frozen', False):
        if hasattr(sys, '_MEIPASS'):
            possible_roots.append(sys._MEIPASS)
        possible_roots.append(os.path.dirname(sys.executable))
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    possible_roots.append(os.path.abspath(os.path.join(current_dir, '..')))
    possible_roots.append(os.path.abspath('.'))

    for root in possible_roots:
        candidates = [
            os.path.join(root, 'documentation', filename),
            os.path.join(root, 'documentation', 'img', filename),
            os.path.join(root, 'img', filename),
            os.path.join(root, filename)
        ]
        for c in candidates:
            if os.path.exists(c):
                return os.path.abspath(c)
    return ""

def open_user_guide():
    """
    Opens the user guide directly in the user's default web browser on GitHub.
    Falls back to opening the local markdown file if offline or if browser launch fails.
    """
    import webbrowser
    url = "https://github.com/tonilogardev/video_to_md_pdf_powerpoint/blob/main/documentation/004_user_guide.md"
    try:
        webbrowser.open(url)
        return
    except Exception:
        pass

    # Offline fallback: open local file
    doc_path = get_asset_path("004_user_guide.md")
    if doc_path and os.path.exists(doc_path):
        try:
            os.startfile(doc_path)
        except Exception:
            pass

def set_window_icon(window):
    """
    Sets the custom application icon on a Tkinter window, replacing
    the default Tkinter feather icon.
    """
    icon_path = get_asset_path("logo.png")
    if icon_path and os.path.exists(icon_path):
        try:
            img = tk.PhotoImage(file=icon_path, master=window)
            window.iconphoto(True, img)
            window._app_logo_icon = img
        except Exception:
            try:
                im = Image.open(icon_path)
                img = ImageTk.PhotoImage(im, master=window)
                window.iconphoto(True, img)
                window._app_logo_icon = img
            except Exception:
                pass

def load_gif_frames(master, filename: str = "logo.gif", size: tuple = (72, 72)):
    """
    Loads all frames of an animated GIF resized to the specified dimensions.
    """
    gif_path = get_asset_path(filename)
    if not gif_path or not os.path.exists(gif_path):
        return []
    
    frames = []
    try:
        im = Image.open(gif_path)
        while True:
            resized = im.copy().convert("RGBA").resize(size, Image.Resampling.LANCZOS)
            frames.append(ImageTk.PhotoImage(resized, master=master))
            im.seek(im.tell() + 1)
    except (EOFError, Exception):
        pass
    return frames
