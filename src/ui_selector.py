import os
import tkinter as tk
from tkinter import filedialog, simpledialog

class UISelector:
    """
    Desktop UI Selector: Uses Tkinter for all user interactions.
    """

    @staticmethod
    def show_main_menu():
        """
        Displays a graphical main menu window with buttons to select input method.
        Falls back to console input if GUI environment is unavailable.
        Returns: '1', '2', '3', or None if cancelled.
        """
        try:
            root = tk.Tk()
            root.title("Video to Markdown & Presentation Converter")
            root.geometry("460x360")
            root.resizable(False, False)
            root.attributes('-topmost', True)

            bg_color = "#f8fafc"
            card_color = "#ffffff"
            text_color = "#0f172a"

            root.configure(bg=bg_color)

            # Center window on screen
            root.update_idletasks()
            width, height = 460, 360
            x = (root.winfo_screenwidth() // 2) - (width // 2)
            y = (root.winfo_screenheight() // 2) - (height // 2)
            root.geometry(f"{width}x{height}+{x}+{y}")

            selected = [None]

            def choose(choice):
                selected[0] = choice
                root.destroy()

            # Header
            header = tk.Frame(root, bg=bg_color, pady=12)
            header.pack(fill="x")

            title_lbl = tk.Label(
                header,
                text="Video to Markdown Converter",
                font=("Segoe UI", 15, "bold"),
                fg=text_color,
                bg=bg_color
            )
            title_lbl.pack()

            sub_lbl = tk.Label(
                header,
                text="Extrae audio, transcripción IA y diapositivas automáticas",
                font=("Segoe UI", 9),
                fg="#64748b",
                bg=bg_color
            )
            sub_lbl.pack(pady=(2, 0))

            # Card
            card = tk.Frame(root, bg=card_color, padx=20, pady=15, highlightthickness=1, highlightbackground="#e2e8f0")
            card.pack(fill="both", expand=True, padx=20, pady=(0, 15))

            card_title = tk.Label(
                card,
                text="Selecciona el origen del vídeo:",
                font=("Segoe UI", 10, "bold"),
                fg=text_color,
                bg=card_color
            )
            card_title.pack(anchor="w", pady=(0, 10))

            btn_style = {
                "font": ("Segoe UI", 10),
                "relief": "flat",
                "cursor": "hand2",
                "padx": 10,
                "pady": 8,
                "anchor": "w"
            }

            b1 = tk.Button(
                card,
                text="1. URL de YouTube (Vídeo o Playlist)",
                bg="#eff6ff",
                fg="#1d4ed8",
                activebackground="#dbeafe",
                command=lambda: choose('1'),
                **btn_style
            )
            b1.pack(fill="x", pady=3)

            b2 = tk.Button(
                card,
                text="2. Seleccionar Archivo(s) de Vídeo Local(es)",
                bg="#f0fdf4",
                fg="#15803d",
                activebackground="#dcfce7",
                command=lambda: choose('2'),
                **btn_style
            )
            b2.pack(fill="x", pady=3)

            b3 = tk.Button(
                card,
                text="3. Seleccionar Carpeta con Vídeos",
                bg="#faf5ff",
                fg="#7e22ce",
                activebackground="#f3e8ff",
                command=lambda: choose('3'),
                **btn_style
            )
            b3.pack(fill="x", pady=3)

            b_cancel = tk.Button(
                card,
                text="Cancelar y Salir",
                bg="#f1f5f9",
                fg="#475569",
                activebackground="#e2e8f0",
                command=root.destroy,
                font=("Segoe UI", 9),
                relief="flat",
                cursor="hand2",
                pady=6
            )
            b_cancel.pack(fill="x", pady=(8, 0))

            root.mainloop()
            return selected[0]

        except Exception:
            print("\nSelect Input Method:")
            print("1. YouTube URL")
            print("2. Local File(s)")
            print("3. Local Directory")
            choice = input("Enter 1, 2, or 3 (or Enter to exit): ").strip()
            return choice if choice in ('1', '2', '3') else None

    @staticmethod
    def select_output_directory(default_dir: str = None) -> str | None:
        """
        Asks the user to choose an output destination directory.
        """
        print("Opening output directory dialog...")
        if not default_dir:
            user_home = os.path.expanduser("~")
            candidates = [
                os.path.join(user_home, "Downloads"),
                os.path.join(user_home, "Desktop"),
                os.getcwd()
            ]
            default_dir = next((c for c in candidates if os.path.exists(c)), os.getcwd())

        try:
            root = tk.Tk()
            root.withdraw()
            root.wm_attributes('-topmost', 1)

            out_dir = filedialog.askdirectory(
                title="Selecciona la carpeta donde guardar los resultados (.zip)",
                initialdir=default_dir
            )
            root.destroy()
            return out_dir.strip() if out_dir else None
        except Exception:
            try:
                out = input(f"Introduce ruta de carpeta de salida [Por defecto: {default_dir}]: ").strip()
                return out if out else default_dir
            except Exception:
                return default_dir

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
        Displays a modern modal dialog to input a YouTube URL with clipboard auto-detection.
        """
        print("Opening URL input dialog...")
        result = [None]

        try:
            root = tk.Tk()
            root.title("Introducir Enlace de YouTube")
            root.geometry("520x240")
            root.resizable(False, False)
            root.attributes('-topmost', True)

            bg_color = "#f8fafc"
            card_color = "#ffffff"
            text_dark = "#0f172a"
            text_muted = "#64748b"
            primary_blue = "#2563eb"
            border_color = "#e2e8f0"

            root.configure(bg=bg_color)

            # Center window
            root.update_idletasks()
            width, height = 520, 240
            x = (root.winfo_screenwidth() // 2) - (width // 2)
            y = (root.winfo_screenheight() // 2) - (height // 2)
            root.geometry(f"{width}x{height}+{x}+{y}")

            # Header
            header = tk.Frame(root, bg=bg_color, pady=10)
            header.pack(fill="x")

            lbl_title = tk.Label(
                header,
                text="Introducir URL de YouTube",
                font=("Segoe UI", 13, "bold"),
                fg=text_dark,
                bg=bg_color
            )
            lbl_title.pack()

            lbl_sub = tk.Label(
                header,
                text="Pega el enlace del vídeo o de la lista de reproducción (Playlist):",
                font=("Segoe UI", 9),
                fg=text_muted,
                bg=bg_color
            )
            lbl_sub.pack(pady=(2, 0))

            # Card
            card = tk.Frame(root, bg=card_color, padx=16, pady=14, highlightthickness=1, highlightbackground=border_color)
            card.pack(fill="both", expand=True, padx=16, pady=(0, 12))

            entry_var = tk.StringVar()
            
            # Check clipboard for convenience
            try:
                clip = root.clipboard_get().strip()
                if any(k in clip.lower() for k in ('youtube.com', 'youtu.be')):
                    entry_var.set(clip)
            except Exception:
                pass

            entry = tk.Entry(
                card,
                textvariable=entry_var,
                font=("Segoe UI", 10),
                bg="#ffffff",
                fg=text_dark,
                relief="solid",
                bd=1,
                highlightthickness=1,
                highlightcolor=primary_blue,
                highlightbackground="#cbd5e1"
            )
            entry.pack(fill="x", ipady=5, pady=(4, 14))
            entry.focus_set()
            if entry_var.get():
                entry.select_range(0, tk.END)

            def on_confirm(event=None):
                val = entry_var.get().strip()
                if val:
                    result[0] = val
                    root.destroy()

            def on_cancel(event=None):
                result[0] = None
                root.destroy()

            root.bind('<Return>', on_confirm)
            root.bind('<Escape>', on_cancel)

            btn_box = tk.Frame(card, bg=card_color)
            btn_box.pack(fill="x")

            btn_confirm = tk.Button(
                btn_box,
                text="Continuar",
                font=("Segoe UI", 9, "bold"),
                bg=primary_blue,
                fg="#ffffff",
                activebackground="#1d4ed8",
                relief="flat",
                cursor="hand2",
                padx=16,
                pady=6,
                command=on_confirm
            )
            btn_confirm.pack(side="right", padx=(8, 0))

            btn_cancel = tk.Button(
                btn_box,
                text="Cancelar",
                font=("Segoe UI", 9),
                bg="#f1f5f9",
                fg="#475569",
                activebackground="#e2e8f0",
                relief="flat",
                cursor="hand2",
                padx=14,
                pady=6,
                command=on_cancel
            )
            btn_cancel.pack(side="right")

            root.mainloop()
            return result[0].strip() if result[0] else ""

        except Exception:
            try:
                url = input("Enter YouTube URL (or press Enter to cancel): ").strip()
                return url
            except Exception:
                return ""

    @staticmethod
    def ask_yes_no(title, question):
        """
        Modern styled Yes/No confirmation dialog with console fallback.
        """
        try:
            root = tk.Tk()
            root.title(title)
            root.geometry("480x240")
            root.resizable(False, False)
            root.attributes('-topmost', True)

            bg_color = "#f8fafc"
            card_color = "#ffffff"
            text_dark = "#0f172a"
            border_color = "#e2e8f0"
            primary_blue = "#2563eb"

            root.configure(bg=bg_color)

            # Center window
            root.update_idletasks()
            width, height = 480, 240
            x = (root.winfo_screenwidth() // 2) - (width // 2)
            y = (root.winfo_screenheight() // 2) - (height // 2)
            root.geometry(f"{width}x{height}+{x}+{y}")

            result = [False]

            def on_yes():
                result[0] = True
                root.destroy()

            def on_no():
                result[0] = False
                root.destroy()

            header = tk.Frame(root, bg=bg_color, pady=10)
            header.pack(fill="x")

            lbl_title = tk.Label(header, text=title, font=("Segoe UI", 12, "bold"), fg=text_dark, bg=bg_color)
            lbl_title.pack()

            card = tk.Frame(root, bg=card_color, padx=16, pady=14, highlightthickness=1, highlightbackground=border_color)
            card.pack(fill="both", expand=True, padx=16, pady=(0, 12))

            lbl_q = tk.Label(card, text=question, font=("Segoe UI", 9), fg="#334155", bg=card_color, wraplength=420, justify="left")
            lbl_q.pack(fill="both", expand=True, pady=(0, 12))

            btn_box = tk.Frame(card, bg=card_color)
            btn_box.pack(fill="x")

            btn_yes = tk.Button(btn_box, text="Sí, procesar lista completa", font=("Segoe UI", 9, "bold"), bg=primary_blue, fg="#ffffff", activebackground="#1d4ed8", relief="flat", cursor="hand2", padx=12, pady=6, command=on_yes)
            btn_yes.pack(side="right", padx=(8, 0))

            btn_no = tk.Button(btn_box, text="No, solo este vídeo", font=("Segoe UI", 9), bg="#f1f5f9", fg="#475569", activebackground="#e2e8f0", relief="flat", cursor="hand2", padx=12, pady=6, command=on_no)
            btn_no.pack(side="right")

            root.bind('<Return>', lambda e: on_yes())
            root.bind('<Escape>', lambda e: on_no())

            root.mainloop()
            return result[0]
        except Exception:
            ans = input(f"{question} (y/n): ").strip().lower()
            return ans in ('y', 'yes', 's', 'si')

    @staticmethod
    def show_error(title: str, message: str):
        """
        Displays a native graphical error dialog (modal, topmost) with console fallback.
        """
        try:
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            root.wm_attributes('-topmost', 1)
            messagebox.showerror(title, message)
            root.destroy()
        except Exception:
            print(f"\n[ERROR - {title}]\n{message}\n")

    @staticmethod
    def show_warning(title: str, message: str):
        """
        Displays a native graphical warning dialog (modal, topmost) with console fallback.
        """
        try:
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            root.wm_attributes('-topmost', 1)
            messagebox.showwarning(title, message)
            root.destroy()
        except Exception:
            print(f"\n[AVISO - {title}]\n{message}\n")

    @staticmethod
    def show_info(title: str, message: str):
        """
        Displays a native graphical info/success dialog (modal, topmost) with console fallback.
        """
        try:
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            root.wm_attributes('-topmost', 1)
            messagebox.showinfo(title, message)
            root.destroy()
        except Exception:
            print(f"\n[INFO - {title}]\n{message}\n")
