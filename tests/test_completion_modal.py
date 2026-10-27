import tkinter as tk
from tkinter import ttk
import os

def show_completion_modal(parent, title, message, output_dir, on_exit=None):
    top = tk.Toplevel(parent)
    top.title(title)
    top.geometry("480x260")
    top.resizable(False, False)
    top.attributes('-topmost', True)

    bg_color = "#f8fafc"
    card_color = "#ffffff"
    text_dark = "#0f172a"
    text_muted = "#64748b"
    primary_blue = "#2563eb"
    success_green = "#16a34a"
    border_color = "#e2e8f0"

    top.configure(bg=bg_color)

    # Center relative to parent or screen
    top.update_idletasks()
    width, height = 480, 260
    x = (top.winfo_screenwidth() // 2) - (width // 2)
    y = (top.winfo_screenheight() // 2) - (height // 2)
    top.geometry(f"{width}x{height}+{x}+{y}")

    # Header with icon
    header = tk.Frame(top, bg=bg_color, pady=12)
    header.pack(fill="x")

    lbl_icon = tk.Label(
        header,
        text="✓",
        font=("Segoe UI", 24, "bold"),
        fg=success_green,
        bg=bg_color
    )
    lbl_icon.pack()

    lbl_title = tk.Label(
        header,
        text=title,
        font=("Segoe UI", 13, "bold"),
        fg=text_dark,
        bg=bg_color
    )
    lbl_title.pack()

    card = tk.Frame(top, bg=card_color, padx=16, pady=12, highlightthickness=1, highlightbackground=border_color)
    card.pack(fill="both", expand=True, padx=18, pady=(0, 14))

    lbl_msg = tk.Label(
        card,
        text=message,
        font=("Segoe UI", 9),
        fg="#334155",
        bg=card_color,
        wraplength=410,
        justify="center"
    )
    lbl_msg.pack(fill="both", expand=True, pady=(0, 10))

    btn_box = tk.Frame(card, bg=card_color)
    btn_box.pack(fill="x")

    def open_dir():
        if output_dir and os.path.exists(output_dir):
            os.startfile(output_dir)

    def close_all():
        top.destroy()
        if on_exit:
            on_exit()

    btn_open = tk.Button(
        btn_box,
        text="📂 Abrir Carpeta de Resultados",
        font=("Segoe UI", 9, "bold"),
        bg=primary_blue,
        fg="#ffffff",
        activebackground="#1d4ed8",
        relief="flat",
        cursor="hand2",
        padx=14,
        pady=6,
        command=open_dir
    )
    btn_open.pack(side="left", expand=True, fill="x", padx=(0, 6))

    btn_exit = tk.Button(
        btn_box,
        text="Salir del Programa",
        font=("Segoe UI", 9, "bold"),
        bg="#0f172a",
        fg="#ffffff",
        activebackground="#334155",
        relief="flat",
        cursor="hand2",
        padx=14,
        pady=6,
        command=close_all
    )
    btn_exit.pack(side="right", expand=True, fill="x")

    # Ring system bell for audible completion notification
    try:
        top.bell()
    except Exception:
        pass

    top.focus_force()
    return top
