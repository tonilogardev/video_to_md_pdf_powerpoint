import os
import sys
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from src.ui_utils import set_window_icon

class ProgressWindow:
    """
    Modern responsive Progress & Status Window for Video to Markdown Converter.
    Handles background processing while keeping the UI responsive without freezing.
    """

    def __init__(self, title="Video to Markdown Converter - Procesando"):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry("580x520")
        self.root.resizable(False, False)
        self.root.attributes('-topmost', True)
        set_window_icon(self.root)

        self.cancelled = False
        self.finished = False
        self.output_dir = None

        # Colors
        self.bg_color = "#f8fafc"
        self.card_color = "#ffffff"
        self.text_dark = "#0f172a"
        self.text_muted = "#64748b"
        self.primary_blue = "#2563eb"
        self.success_green = "#16a34a"
        self.border_color = "#e2e8f0"

        self.root.configure(bg=self.bg_color)

        # Center on screen
        self.root.update_idletasks()
        width, height = 580, 520
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        self._build_ui()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close_requested)

    def _build_ui(self):
        # 1. Header (Top)
        header = tk.Frame(self.root, bg=self.bg_color, pady=10)
        header.pack(side="top", fill="x")

        self.lbl_title = tk.Label(
            header,
            text="Procesando Conversión de Vídeo",
            font=("Segoe UI", 14, "bold"),
            fg=self.text_dark,
            bg=self.bg_color
        )
        self.lbl_title.pack()

        self.lbl_subtitle = tk.Label(
            header,
            text="Iniciando componentes y preparando archivos...",
            font=("Segoe UI", 9),
            fg=self.text_muted,
            bg=self.bg_color
        )
        self.lbl_subtitle.pack(pady=(2, 0))

        # 2. Footer (Bottom) - Packed before card so it is NEVER cut off
        self.footer = tk.Frame(self.root, bg=self.bg_color, padx=18, pady=10)
        self.footer.pack(side="bottom", fill="x")

        self.lbl_footer_status = tk.Label(
            self.footer,
            text="Por favor, no cierres esta ventana mientras la IA procesa el vídeo...",
            font=("Segoe UI", 8),
            fg=self.text_muted,
            bg=self.bg_color
        )
        self.lbl_footer_status.pack(side="left", pady=4)

        self.btn_frame = tk.Frame(self.footer, bg=self.bg_color)
        self.btn_frame.pack(side="right")

        self.btn_cancel = tk.Button(
            self.btn_frame,
            text="Cancelar y Salir",
            font=("Segoe UI", 9),
            bg="#f1f5f9",
            fg="#dc2626",
            activebackground="#fee2e2",
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=5,
            command=self._on_close_requested
        )
        self.btn_cancel.pack(side="left")

        # 3. Card container (Center) - Expands to fill available middle space
        card = tk.Frame(self.root, bg=self.card_color, padx=18, pady=12,
                        highlightthickness=1, highlightbackground=self.border_color)
        card.pack(side="top", fill="both", expand=True, padx=18, pady=(0, 6))

        # Current Status label
        self.lbl_current_step = tk.Label(
            card,
            text="Estado: Preparando...",
            font=("Segoe UI", 10, "bold"),
            fg=self.primary_blue,
            bg=self.card_color,
            anchor="w"
        )
        self.lbl_current_step.pack(fill="x", pady=(0, 6))

        # Progress bar
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Custom.Horizontal.TProgressbar",
                        thickness=14,
                        troughcolor="#e2e8f0",
                        background=self.primary_blue)

        self.progress_bar = ttk.Progressbar(
            card,
            style="Custom.Horizontal.TProgressbar",
            orient="horizontal",
            mode="determinate",
            maximum=100
        )
        self.progress_bar.pack(fill="x", pady=(0, 8))

        # Live log header
        lbl_log = tk.Label(
            card,
            text="Registro de actividad en tiempo real:",
            font=("Segoe UI", 9, "bold"),
            fg=self.text_dark,
            bg=self.card_color,
            anchor="w"
        )
        lbl_log.pack(fill="x", pady=(0, 4))

        # Log container
        log_frame = tk.Frame(card, bg="#f1f5f9", highlightthickness=1, highlightbackground=self.border_color)
        log_frame.pack(fill="both", expand=True)

        self.txt_log = tk.Text(
            log_frame,
            wrap="word",
            font=("Consolas", 8),
            bg="#f8fafc",
            fg="#334155",
            padx=8,
            pady=6,
            relief="flat",
            state="disabled",
            height=10
        )
        scroll = tk.Scrollbar(log_frame, command=self.txt_log.yview)
        self.txt_log.configure(yscrollcommand=scroll.set)

        scroll.pack(side="right", fill="y")
        self.txt_log.pack(side="left", fill="both", expand=True)

    def log(self, message: str):
        """Thread-safe logging to the text area."""
        def _append():
            try:
                if not self.root or not self.root.winfo_exists():
                    return
                self.txt_log.configure(state="normal")
                timestamp = time.strftime("%H:%M:%S")
                self.txt_log.insert("end", f"[{timestamp}] {message}\n")
                self.txt_log.see("end")
                self.txt_log.configure(state="disabled")
            except Exception:
                pass

        if self.root:
            try:
                self.root.after(0, _append)
            except Exception:
                pass

    def set_progress(self, percent: float, step_text: str = None, subtitle: str = None):
        """Thread-safe progress update."""
        def _update():
            try:
                if not self.root or not self.root.winfo_exists():
                    return
                self.progress_bar["value"] = percent
                if step_text:
                    self.lbl_current_step.config(text=f"Estado: {step_text}")
                if subtitle:
                    self.lbl_subtitle.config(text=subtitle)
            except Exception:
                pass

        if self.root:
            try:
                self.root.after(0, _update)
            except Exception:
                pass

    def set_finished(self, success: bool, message: str, output_dir: str = None):
        """Thread-safe completion handler."""
        self.finished = True
        self.output_dir = output_dir

        def _finish():
            try:
                if not self.root or not self.root.winfo_exists():
                    return
                if success:
                    self.progress_bar["value"] = 100
                    self.lbl_title.config(text="¡Conversión Completada con Éxito!", fg=self.success_green)
                    self.lbl_subtitle.config(text=message, fg=self.success_green)
                    self.lbl_current_step.config(text="Proceso finalizado al 100%", fg=self.success_green)
                    self.lbl_footer_status.config(text="Todos los archivos han sido generados y empaquetados.")
                else:
                    self.lbl_title.config(text="Ocurrió un error en el proceso", fg="#dc2626")
                    self.lbl_subtitle.config(text=message, fg="#dc2626")
                    self.lbl_current_step.config(text="Error durante la ejecución", fg="#dc2626")
                    self.lbl_footer_status.config(text="Revisa el registro de actividad para más detalles.")

                # Clear in-progress buttons (like Cancel) from background window footer
                for child in self.btn_frame.winfo_children():
                    child.destroy()

                # Show floating completion modal window that blocks background interaction
                self._show_completion_popup(success, message, output_dir)
            except Exception:
                pass

        if self.root:
            try:
                self.root.after(0, _finish)
            except Exception:
                pass

    def _show_completion_popup(self, success: bool, message: str, output_dir: str = None):
        """
        Displays a prominent floating completion modal window that strictly locks
        the progress window behind it, eliminating duplicate action buttons.
        """
        popup = tk.Toplevel(self.root)
        popup.title("¡Tarea Completada!" if success else "Aviso de Finalización")
        popup.geometry("500x260")
        popup.resizable(False, False)
        popup.transient(self.root)
        popup.attributes('-topmost', True)
        popup.configure(bg=self.bg_color)
        set_window_icon(popup)

        # Center on screen
        popup.update_idletasks()
        w, h = 500, 260
        x = (popup.winfo_screenwidth() // 2) - (w // 2)
        y = (popup.winfo_screenheight() // 2) - (h // 2)
        popup.geometry(f"{w}x{h}+{x}+{y}")

        # Audible notification chime
        try:
            popup.bell()
        except Exception:
            pass

        # Header
        header = tk.Frame(popup, bg=self.bg_color, pady=10)
        header.pack(fill="x")

        icon = "✓" if success else "⚠️"
        icon_color = self.success_green if success else "#dc2626"
        lbl_icon = tk.Label(header, text=icon, font=("Segoe UI", 24, "bold"), fg=icon_color, bg=self.bg_color)
        lbl_icon.pack()

        lbl_title = tk.Label(
            header,
            text="¡Conversión Finalizada con Éxito!" if success else "El proceso finalizó con incidencias",
            font=("Segoe UI", 13, "bold"),
            fg=self.text_dark,
            bg=self.bg_color
        )
        lbl_title.pack(pady=(2, 0))

        # Card
        card = tk.Frame(popup, bg=self.card_color, padx=16, pady=12, highlightthickness=1, highlightbackground=self.border_color)
        card.pack(fill="both", expand=True, padx=16, pady=(0, 14))

        lbl_desc = tk.Label(
            card,
            text=message,
            font=("Segoe UI", 9),
            fg="#334155",
            bg=self.card_color,
            wraplength=440,
            justify="center"
        )
        lbl_desc.pack(fill="both", expand=True, pady=(0, 10))

        # Action Buttons inside popup (the ONLY visible action buttons)
        btn_box = tk.Frame(card, bg=self.card_color)
        btn_box.pack(fill="x")

        def _open():
            if output_dir and os.path.exists(output_dir):
                try:
                    os.startfile(output_dir)
                except Exception:
                    pass

        def _exit_app():
            try:
                popup.grab_release()
            except Exception:
                pass
            popup.destroy()
            self.root.destroy()

        def _on_modal_close():
            try:
                popup.grab_release()
            except Exception:
                pass
            popup.destroy()
            # If user closes modal with 'X' to inspect logs, unblock background window and show close button
            self._setup_unblocked_footer(success, output_dir)

        popup.protocol("WM_DELETE_WINDOW", _on_modal_close)

        if output_dir and os.path.exists(output_dir) and success:
            btn_open = tk.Button(
                btn_box,
                text="📂 Abrir Carpeta de Resultados",
                font=("Segoe UI", 9, "bold"),
                bg=self.primary_blue,
                fg="#ffffff",
                activebackground="#1d4ed8",
                relief="flat",
                cursor="hand2",
                padx=12,
                pady=6,
                command=_open
            )
            btn_open.pack(side="left", expand=True, fill="x", padx=(0, 8))

        btn_exit = tk.Button(
            btn_box,
            text="Salir de la Aplicación",
            font=("Segoe UI", 9, "bold"),
            bg="#0f172a" if success else "#dc2626",
            fg="#ffffff",
            activebackground="#334155",
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=6,
            command=_exit_app
        )
        btn_exit.pack(side="right", expand=True, fill="x")

        # Strictly lock focus to modal dialog
        popup.grab_set()
        popup.focus_force()

    def _setup_unblocked_footer(self, success: bool, output_dir: str = None):
        """
        Populates a clean button on the background window only if the user explicitly
        dismissed the modal dialog to inspect the log.
        """
        for child in self.btn_frame.winfo_children():
            child.destroy()

        if output_dir and os.path.exists(output_dir) and success:
            btn_open = tk.Button(
                self.btn_frame,
                text="📂 Abrir Carpeta",
                font=("Segoe UI", 9, "bold"),
                bg=self.primary_blue,
                fg="#ffffff",
                activebackground="#1d4ed8",
                relief="flat",
                cursor="hand2",
                padx=12,
                pady=5,
                command=self._open_output_dir
            )
            btn_open.pack(side="left", padx=(0, 6))

        btn_exit = tk.Button(
            self.btn_frame,
            text="Cerrar Aplicación",
            font=("Segoe UI", 9, "bold"),
            bg="#0f172a" if success else "#dc2626",
            fg="#ffffff",
            activebackground="#334155",
            relief="flat",
            cursor="hand2",
            padx=14,
            pady=5,
            command=self.root.destroy
        )
        btn_exit.pack(side="left")
        self.lbl_footer_status.config(text="Puedes revisar el registro de actividad o cerrar.")

    def _open_output_dir(self):
        if self.output_dir and os.path.exists(self.output_dir):
            try:
                os.startfile(self.output_dir)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir la carpeta: {e}")

    def _on_close_requested(self):
        if self.finished:
            self.root.destroy()
        else:
            if messagebox.askyesno("Confirmar Salida", "¿Seguro que deseas cancelar el proceso en curso?"):
                self.cancelled = True
                self.root.destroy()

    def start_worker(self, worker_func):
        """
        Runs worker_func in a background thread and starts the Tkinter event loop.
        worker_func receives `self` as its first parameter.
        """
        thread = threading.Thread(target=worker_func, args=(self,), daemon=True)
        thread.start()
        self.root.mainloop()
