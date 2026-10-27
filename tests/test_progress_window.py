import time
import sys
import os

sys.path.append(os.path.abspath('.'))
from src.progress_window import ProgressWindow

def simulate_pipeline(pw: ProgressWindow):
    try:
        pw.log("Inicializando entorno de trabajo...")
        pw.set_progress(10, "Iniciando descargas...")
        time.sleep(0.5)

        pw.log("Descargando vídeo: https://www.youtube.com/watch?v=demo")
        pw.set_progress(25, "Descarga completada")
        time.sleep(0.5)

        pw.log("Extrayendo pista de audio a formato MP3...")
        pw.set_progress(40, "Audio extraído con éxito")
        time.sleep(0.5)

        pw.log("Transcribiendo audio con Whisper AI (modelo small)...")
        pw.set_progress(60, "Transcribiendo con Inteligencia Artificial...")
        time.sleep(0.5)

        pw.log("Whisper: 48 segmentos transcritos en español.")
        pw.set_progress(75, "Extrayendo diapositivas con SSIM...")
        time.sleep(0.5)

        pw.log("Se detectaron 14 diapositivas únicas.")
        pw.log("Generando Markdown, PDF y presentación PowerPoint...")
        pw.set_progress(90, "Generando documentos...")
        time.sleep(0.5)

        pw.log("Empaquetando todo en ZIP final...")
        pw.set_progress(100, "Finalizando...")
        time.sleep(0.5)

        pw.log("¡Proceso completado con éxito! Archivo: demo_package.zip")
        pw.set_finished(True, "Se ha procesado 1 vídeo correctamente.", output_dir=".")

    except Exception as e:
        pw.log(f"Error: {e}")
        pw.set_finished(False, str(e))

if __name__ == '__main__':
    pw = ProgressWindow("Test Progress Window")
    # Close automatically after 4 seconds
    pw.root.after(4000, pw.root.destroy)
    pw.start_worker(simulate_pipeline)
    print("Test finished cleanly.")
