import tkinter as tk
from tkinter import filedialog, simpledialog

class UISelector:
    """
    Desktop UI Selector: Uses Tkinter for all user interactions.
    """

    @staticmethod
    def select_files():
        """
        Opens a system file dialog to select multiple video files.
        """
        print("Opening file dialog...")
        root = tk.Tk()
        root.withdraw() # Hide the main window
        root.wm_attributes('-topmost', 1) 

        file_paths = filedialog.askopenfilenames(
            title="Select Video Files",
            filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv *.webm"), ("All files", "*.*")]
        )
        root.destroy()
        return list(file_paths)

    @staticmethod
    def select_directory():
        """
        Opens a system file dialog to select a directory.
        """
        print("Opening directory dialog...")
        root = tk.Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1) 

        dir_path = filedialog.askdirectory(title="Select Directory with Video Files")
        root.destroy()
        return dir_path

    @staticmethod
    def get_youtube_url():
        """
        Opens a simple input dialog to get YouTube URL.
        """
        print("Opening URL input dialog...")
        root = tk.Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)

        url = simpledialog.askstring("YouTube Input", "Enter YouTube URL (Single or Playlist):")
        root.destroy()
        return url.strip() if url else ""

    @staticmethod
    def ask_yes_no(title, question):
        """
        Simple Yes/No dialog.
        """
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)
        
        response = messagebox.askyesno(title, question)
        root.destroy()
        return response
