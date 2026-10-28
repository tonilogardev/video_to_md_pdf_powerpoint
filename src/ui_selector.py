import os
import tkinter as tk
from tkinter import filedialog, simpledialog
from src.ui_utils import set_window_icon, load_gif_frames, open_user_guide

class UISelector:
    """
    Desktop UI Selector: Uses Tkinter for all user interactions.
    """

    @staticmethod
    def show_main_menu():
        """
        Displays a graphical main menu window with animated logo,
        clear explanation of generated output files, and input source buttons.
        Falls back to console input if GUI environment is unavailable.
        Returns: '1', '2', '3', or None if cancelled.
        """
        try:
            root = tk.Tk()
            root.title("Video to Markdown & Presentation Suite")
            root.geometry("560x720")
            root.resizable(False, False)
            root.attributes('-topmost', True)
            set_window_icon(root)

            bg_color = "#f8fafc"
            card_color = "#ffffff"
            text_color = "#0f172a"

            root.configure(bg=bg_color)

            # Center window on screen
            root.update_idletasks()
            width, height = 560, 720
            x = (root.winfo_screenwidth() // 2) - (width // 2)
            y = (root.winfo_screenheight() // 2) - (height // 2)
            root.geometry(f"{width}x{height}+{x}+{y}")

            selected = [None]
            anim_job = [None]

            def _clean_and_destroy(val=None):
                selected[0] = val
                if anim_job[0]:
                    try:
                        root.after_cancel(anim_job[0])
                    except Exception:
                        pass
                    anim_job[0] = None
                try:
                    if 'lbl_gif' in locals() and lbl_gif.winfo_exists():
                        lbl_gif.config(image="")
                except Exception:
                    pass
                if 'gif_frames' in locals() and gif_frames:
                    gif_frames.clear()
                try:
                    root.destroy()
                except Exception:
                    pass

            def choose(choice):
                _clean_and_destroy(choice)

            root.protocol("WM_DELETE_WINDOW", lambda: _clean_and_destroy(None))

            # Header with animated GIF
            header = tk.Frame(root, bg=bg_color, pady=8)
            header.pack(fill="x")

            gif_frames = load_gif_frames(root, "logo.gif", size=(72, 72))
            if gif_frames:
                lbl_gif = tk.Label(header, image=gif_frames[0], bg=bg_color)
                lbl_gif.pack()

                def _animate(idx=0):
                    try:
                        if root.winfo_exists() and lbl_gif.winfo_exists() and gif_frames:
                            lbl_gif.config(image=gif_frames[idx])
                            anim_job[0] = root.after(80, _animate, (idx + 1) % len(gif_frames))
                    except Exception:
                        pass

                anim_job[0] = root.after(80, _animate, 1)

            title_lbl = tk.Label(
                header,
                text="Video to Markdown & Presentation Suite",
                font=("Segoe UI", 14, "bold"),
                fg=text_color,
                bg=bg_color
            )
            title_lbl.pack(pady=(4, 0))

            sub_lbl = tk.Label(
                header,
                text="Transforma tus vídeos en material de estudio y presentaciones estructuradas",
                font=("Segoe UI", 9),
                fg="#64748b",
                bg=bg_color
            )
            sub_lbl.pack(pady=(1, 0))

            btn_help = tk.Button(
                header,
                text="📖 Guía de uso",
                font=("Segoe UI", 9, "underline bold"),
                fg="#2563eb",
                bg=bg_color,
                activeforeground="#1d4ed8",
                activebackground=bg_color,
                relief="flat",
                bd=0,
                cursor="hand2",
                command=open_user_guide
            )
            btn_help.pack(pady=(4, 0))

            # Info Card: Detailed explanation of output files
            info_card = tk.Frame(root, bg=card_color, padx=16, pady=10, highlightthickness=1, highlightbackground="#e2e8f0")
            info_card.pack(fill="x", padx=20, pady=(0, 10))

            lbl_info_title = tk.Label(
                info_card,
                text="📦 Archivos generados a partir de los vídeos (en paquete final .ZIP):",
                font=("Segoe UI", 9, "bold"),
                fg="#1e293b",
                bg=card_color
            )
            lbl_info_title.pack(anchor="w", pady=(0, 6))

            files_info = [
                ("📁 frames/", "Carpeta con capturas automáticas de diapositivas (SSIM)"),
                ("📝 001.md", "Documento Markdown estructurado con capturas adjuntas"),
                ("📄 001.pdf", "Documento PDF maquetado con imágenes y texto sincronizado"),
                ("📊 001.pptx", "Presentación PowerPoint (captura a izq. y texto a der.)"),
                ("🎵 001.mp3", "Pista de audio extraída del vídeo en alta fidelidad"),
                ("💬 001.srt", "Subtítulos sincronizados temporalmente con Whisper AI"),
                ("🎬 001.mp4", "Vídeo original normalizado y optimizado"),
            ]

            info_grid = tk.Frame(info_card, bg=card_color)
            info_grid.pack(fill="x")

            for i, (ext, desc) in enumerate(files_info):
                row_bg = "#f8fafc" if i % 2 == 0 else "#ffffff"
                row_f = tk.Frame(info_grid, bg=row_bg, padx=6, pady=2)
                row_f.pack(fill="x", pady=1)

                lbl_tag = tk.Label(
                    row_f,
                    text=ext,
                    font=("Segoe UI", 8, "bold"),
                    fg="#2563eb",
                    bg=row_bg,
                    width=12,
                    anchor="w"
                )
                lbl_tag.pack(side="left")

                lbl_desc = tk.Label(
                    row_f,
                    text=desc,
                    font=("Segoe UI", 8),
                    fg="#475569",
                    bg=row_bg,
                    anchor="w"
                )
                lbl_desc.pack(side="left", fill="x", expand=True)

            # Action Card: Source selector buttons
            card = tk.Frame(root, bg=card_color, padx=16, pady=12, highlightthickness=1, highlightbackground="#e2e8f0")
            card.pack(fill="both", expand=True, padx=20, pady=(0, 14))

            card_title = tk.Label(
                card,
                text="Selecciona el origen del vídeo a procesar:",
                font=("Segoe UI", 9, "bold"),
                fg=text_color,
                bg=card_color
            )
            card_title.pack(anchor="w", pady=(0, 8))

            btn_style = {
                "font": ("Segoe UI", 9, "bold"),
                "relief": "flat",
                "cursor": "hand2",
                "padx": 10,
                "pady": 7,
                "anchor": "w"
            }

            b1 = tk.Button(
                card,
                text="1. URL de YouTube (Vídeo individual o Lista de reproducción)",
                bg="#eff6ff",
                fg="#1d4ed8",
                activebackground="#dbeafe",
                command=lambda: choose('1'),
                **btn_style
            )
            b1.pack(fill="x", pady=2)

            b2 = tk.Button(
                card,
                text="2. Seleccionar Archivo(s) de Vídeo Local(es)",
                bg="#f0fdf4",
                fg="#15803d",
                activebackground="#dcfce7",
                command=lambda: choose('2'),
                **btn_style
            )
            b2.pack(fill="x", pady=2)

            b3 = tk.Button(
                card,
                text="3. Seleccionar Carpeta con Vídeos (Lotes)",
                bg="#faf5ff",
                fg="#7e22ce",
                activebackground="#f3e8ff",
                command=lambda: choose('3'),
                **btn_style
            )
            b3.pack(fill="x", pady=2)

            b_cancel = tk.Button(
                card,
                text="Cancelar y Salir",
                bg="#f1f5f9",
                fg="#475569",
                activebackground="#e2e8f0",
                command=lambda: _clean_and_destroy(None),
                font=("Segoe UI", 9),
                relief="flat",
                cursor="hand2",
                pady=5
            )
            b_cancel.pack(fill="x", pady=(8, 0))

            root.mainloop()
            import gc
            gc.collect()
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
            set_window_icon(root)

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

            # Menú contextual con el botón derecho (Cortar, Copiar, Pegar, Seleccionar todo)
            context_menu = tk.Menu(entry, tearoff=0, font=("Segoe UI", 9))

            def _paste():
                try:
                    text = root.clipboard_get()
                    try:
                        entry.delete(tk.SEL_FIRST, tk.SEL_LAST)
                    except tk.TclError:
                        pass
                    entry.insert(tk.INSERT, text)
                except Exception:
                    pass

            def _copy():
                try:
                    text = entry.selection_get()
                    root.clipboard_clear()
                    root.clipboard_append(text)
                except Exception:
                    pass

            def _cut():
                try:
                    text = entry.selection_get()
                    root.clipboard_clear()
                    root.clipboard_append(text)
                    entry.delete(tk.SEL_FIRST, tk.SEL_LAST)
                except Exception:
                    pass

            def _select_all():
                entry.select_range(0, tk.END)
                entry.icursor(tk.END)

            context_menu.add_command(label="Cortar", command=_cut, accelerator="Ctrl+X")
            context_menu.add_command(label="Copiar", command=_copy, accelerator="Ctrl+C")
            context_menu.add_command(label="Pegar", command=_paste, accelerator="Ctrl+V")
            context_menu.add_separator()
            context_menu.add_command(label="Seleccionar todo", command=_select_all, accelerator="Ctrl+A")

            def show_context_menu(event):
                entry.focus_set()
                # Si no hay texto seleccionado, posicionar cursor donde se hizo clic
                try:
                    if not entry.selection_present():
                        entry.icursor(f"@{event.x}")
                except Exception:
                    pass

                # Comprobar si hay contenido en el portapapeles para habilitar/deshabilitar "Pegar"
                try:
                    clip_content = root.clipboard_get()
                    context_menu.entryconfig("Pegar", state="normal" if clip_content else "disabled")
                except Exception:
                    context_menu.entryconfig("Pegar", state="disabled")

                # Comprobar si hay texto seleccionado para habilitar/deshabilitar "Cortar" y "Copiar"
                try:
                    has_sel = bool(entry.selection_get())
                except Exception:
                    has_sel = False

                context_menu.entryconfig("Cortar", state="normal" if has_sel else "disabled")
                context_menu.entryconfig("Copiar", state="normal" if has_sel else "disabled")

                try:
                    context_menu.tk_popup(event.x_root, event.y_root)
                finally:
                    context_menu.grab_release()

            entry.bind("<Button-3>", show_context_menu)

            def on_confirm(event=None):
                val = entry_var.get().strip()
                if not val:
                    return
                # Verify that it looks like a YouTube link
                if not any(k in val.lower() for k in ('youtube.com', 'youtu.be', 'http://', 'https://')):
                    lbl_sub.config(
                        text="⚠️ Por favor, introduce un enlace válido de YouTube (ej: https://www.youtube.com/watch?v=...)",
                        fg="#dc2626"
                    )
                    return
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
            set_window_icon(root)

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
