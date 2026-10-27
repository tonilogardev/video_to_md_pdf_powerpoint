import os
import sys

# Ensure UTF-8 output and suppress flashing MS-DOS/CMD console windows on Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

    try:
        import subprocess
        _orig_popen_init = subprocess.Popen.__init__

        def _silent_popen_init(self, *args, **kwargs):
            # CREATE_NO_WINDOW (0x08000000) prevents command prompt flashing
            creationflags = kwargs.get('creationflags', 0)
            creationflags |= getattr(subprocess, 'CREATE_NO_WINDOW', 0x08000000)
            kwargs['creationflags'] = creationflags
            return _orig_popen_init(self, *args, **kwargs)

        subprocess.Popen.__init__ = _silent_popen_init
    except Exception:
        pass

# Ensure we can import from src
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.input_handler import InputHandler
from src.converter import VideoConverter
from src.audio_extractor import AudioExtractor
from src.transcriber import Transcriber
from src.frame_extractor import FrameExtractor
from src.markdown_gen import MarkdownGenerator
from src.packager import Packager
from src.ui_selector import UISelector
from src.pdf_gen import PdfGenerator
from src.ppt_gen import PptGenerator
from src.ffmpeg_installer import ensure_ffmpeg
from src.progress_window import ProgressWindow

def main():
    print("========================================")
    print("   Video to Markdown Converter (Desktop)")
    print("========================================")
    # Ensure ffmpeg is available (attempt automatic install on Windows if missing)
    ffmpeg_path = ensure_ffmpeg()
    if ffmpeg_path:
        # If a downloaded or local absolute path was returned, add its folder to PATH
        # so subprocess calls to 'ffmpeg' (used by Whisper, yt-dlp, and other libs) succeed.
        if os.path.isabs(ffmpeg_path) and os.path.exists(ffmpeg_path):
            ffmpeg_dir = os.path.dirname(ffmpeg_path)
            os.environ['PATH'] = ffmpeg_dir + os.pathsep + os.environ.get('PATH', '')
            os.environ['FFMPEG_PATH'] = ffmpeg_path
            print(f"Added {ffmpeg_dir} to PATH for this session.")
        else:
            import shutil
            which_p = shutil.which('ffmpeg')
            if which_p:
                os.environ['FFMPEG_PATH'] = which_p
                os.environ['PATH'] = os.path.dirname(which_p) + os.pathsep + os.environ.get('PATH', '')
            else:
                os.environ['FFMPEG_PATH'] = 'ffmpeg'
            print("ffmpeg is available on system PATH.")
    else:
        print("Warning: ffmpeg not available. Audio extraction will fail until ffmpeg is installed.")
        UISelector.show_warning("FFmpeg no encontrado", "FFmpeg no está disponible en el sistema. La extracción de audio y conversión fallarán hasta que instales FFmpeg.")
    
    # 1. Select Input Source via GUI Main Menu
    choice = UISelector.show_main_menu()
    if not choice:
        print("No input method selected. Exiting.")
        return

    sources = []
    process_playlist = False

    if choice == '1':
        url = UISelector.get_youtube_url()
        if not url:
            print("No URL entered. Exiting.")
            return

        if "list=" in url:
            if UISelector.ask_yes_no("Playlist Detectada", "¿Deseas procesar la lista de reproducción completa?"):
                process_playlist = True
                
        sources.append(url)
        
    elif choice == '2':
        sources = UISelector.select_files()
        if not sources:
            print("No files selected. Exiting.")
            return
            
    elif choice == '3':
        dir_path = UISelector.select_directory()
        if not dir_path:
            print("No directory selected. Exiting.")
            return
            
        print(f"Scanning directory: {dir_path}")
        valid_exts = ('.mp4', '.avi', '.mov', '.mkv', '.webm')
        for file in os.listdir(dir_path):
            if file.lower().endswith(valid_exts):
                sources.append(os.path.join(dir_path, file))
                
        if not sources:
            print("No video files found in the selected directory. Exiting.")
            UISelector.show_warning("Sin vídeos", f"No se encontraron archivos de vídeo compatibles en:\n{dir_path}")
            return
            
    else:
        print("Invalid choice. Exiting.")
        return

    # 2. Select Output Destination Directory (Always asked as requested)
    output_dir = UISelector.select_output_directory()
    if not output_dir:
        print("No output directory selected. Exiting.")
        UISelector.show_warning("Cancelado", "No se seleccionó ninguna carpeta de salida para los resultados.")
        return

    os.makedirs(output_dir, exist_ok=True)
    print(f"Directorio de salida: {output_dir}")

    # Isolated temporary workspace inside output_dir
    work_dir = os.path.join(output_dir, "_temp_workspace")
    os.makedirs(work_dir, exist_ok=True)
    frames_dir = os.path.join(work_dir, "frames")

    pw = ProgressWindow("Video to Markdown Converter - Procesando")

    def worker(pw: ProgressWindow):
        try:
            pw.log("Inicializando componentes y espacio temporal de trabajo...")
            pw.set_progress(5, "Iniciando descarga y análisis de vídeos...", "Paso 1: Procesando entradas")

            # 3. Init Modules
            input_handler = InputHandler(output_dir=os.path.join(work_dir, "downloads"), ffmpeg_location=ffmpeg_path)
            frame_extractor = FrameExtractor(output_folder=frames_dir)
            markdown_gen = MarkdownGenerator()
            pdf_gen = PdfGenerator()
            ppt_gen = PptGenerator()

            # 4. Processing Loop
            pw.log(f"Fuentes recibidas: {len(sources)}")
            video_files = input_handler.process_input(sources, process_playlist=process_playlist)

            if pw.cancelled:
                pw.log("Operación cancelada por el usuario.")
                return

            if not video_files:
                pw.log("No se encontraron vídeos válidos para procesar.")
                pw.set_finished(False, "No se encontraron vídeos válidos para procesar.", output_dir=output_dir)
                return

            total_vids = len(video_files)
            pw.log(f"Se encontraron {total_vids} vídeo(s) para procesar.")
            pw.set_progress(15, "Cargando modelo Whisper AI...", f"0/{total_vids} vídeos procesados")

            transcriber = Transcriber(model_size="small")

            successful_videos = []
            failed_videos = []

            for i, video_path in enumerate(video_files):
                if pw.cancelled:
                    pw.log("Cancelación solicitada por el usuario.")
                    break

                video_name = os.path.basename(video_path)
                base_pct = 15 + int((i / total_vids) * 80)
                step_range = int(80 / total_vids)

                pw.log(f"\n--- [{i+1}/{total_vids}] Iniciando: {video_name} ---")
                pw.set_progress(base_pct, f"Preparando vídeo {i+1} de {total_vids}...", f"[{i+1}/{total_vids}] {video_name}")

                try:
                    # Convert
                    mp4_path = VideoConverter.ensure_mp4(video_path)
                    video_title = os.path.splitext(os.path.basename(mp4_path))[0]
                    
                    # Audio
                    pw.set_progress(base_pct + int(step_range * 0.15), "Extrayendo audio MP3...", f"[{i+1}/{total_vids}] {video_title}")
                    audio_path = AudioExtractor.extract_audio(mp4_path, output_path=os.path.join(work_dir, f"{video_title}.mp3"))
                    if not audio_path:
                        raise RuntimeError(f"No se pudo extraer el audio del vídeo: {video_path}")
                    pw.log("Pista de audio extraída con éxito.")
                    
                    if pw.cancelled: break

                    # Transcribe
                    pw.set_progress(base_pct + int(step_range * 0.35), "Transcribiendo con Whisper AI...", f"[{i+1}/{total_vids}] {video_title}")
                    pw.log("Transcribiendo contenido hablado con Whisper AI (puede tomar unos momentos)...")
                    transcription_result = transcriber.transcribe(audio_path)
                    num_segments = len(transcription_result.get('segments', []))
                    pw.log(f"Transcripción finalizada: {num_segments} segmentos detectados.")

                    srt_path = os.path.join(work_dir, f"{video_title}.srt")
                    transcriber.save_srt(transcription_result['segments'], srt_path)
                    
                    if pw.cancelled: break

                    # Smart Frames
                    pw.set_progress(base_pct + int(step_range * 0.60), "Detectando diapositivas (SSIM)...", f"[{i+1}/{total_vids}] {video_title}")
                    pw.log("Analizando fotogramas visuales con SSIM...")
                    slides = frame_extractor.extract_frames(mp4_path)
                    pw.log(f"Se extrajeron {len(slides)} diapositivas visuales clave.")
                    
                    if pw.cancelled: break

                    # Markdown & PDF
                    pw.set_progress(base_pct + int(step_range * 0.75), "Generando Markdown y PDF...", f"[{i+1}/{total_vids}] {video_title}")
                    md_path = os.path.join(work_dir, f"{video_title}.md")
                    markdown_gen.generate_md(video_title, transcription_result['segments'], slides, output_path=md_path)
                    pw.log("Documento Markdown generado con marcas de tiempo.")
                    
                    pdf_path = os.path.join(work_dir, f"{video_title}.pdf")
                    pdf_gen.generate_pdf(md_path, pdf_path)
                    pw.log("Documento PDF exportado con éxito.")
                    
                    if pw.cancelled: break

                    # PowerPoint
                    pw.set_progress(base_pct + int(step_range * 0.85), "Creando presentación PowerPoint...", f"[{i+1}/{total_vids}] {video_title}")
                    ppt_path = os.path.join(work_dir, f"{video_title}.pptx")
                    ppt_gen.generate_ppt(video_title, transcription_result['segments'], slides, ppt_path)
                    pw.log("Presentación PowerPoint (.pptx) generada con éxito.")
                    
                    # Package into user-selected output_dir
                    pw.set_progress(base_pct + int(step_range * 0.95), "Empaquetando archivo ZIP final...", f"[{i+1}/{total_vids}] {video_title}")
                    files_to_zip = [mp4_path, audio_path, srt_path, md_path, pdf_path, ppt_path]
                    zip_name = os.path.join(output_dir, f"{video_title}_package.zip")
                    Packager.create_package(zip_name, files_to_include=files_to_zip, folder_to_include=frames_dir)
                    
                    pw.log(f"¡PAQUETE ZIP GENERADO!: {os.path.basename(zip_name)}")
                    successful_videos.append(zip_name)
                    
                    # Clean up intermediate video-specific files
                    for f in [audio_path, srt_path, md_path, pdf_path, ppt_path]:
                        if os.path.exists(f):
                            os.remove(f)
                    import shutil
                    if os.path.exists(frames_dir):
                        shutil.rmtree(frames_dir, ignore_errors=True)

                except Exception as e:
                    pw.log(f"ERROR al procesar {video_name}: {e}")
                    failed_videos.append((video_path, str(e)))

            # Clean up workspace folder
            import gc, shutil
            gc.collect()
            if os.path.exists(work_dir):
                shutil.rmtree(work_dir, ignore_errors=True)

            if pw.cancelled:
                pw.log("El proceso fue detenido por el usuario.")
                pw.set_finished(False, "Proceso cancelado por el usuario.", output_dir=output_dir)
                return

            if successful_videos:
                pw.set_progress(100, "¡Conversión finalizada!", f"{len(successful_videos)} de {total_vids} vídeos procesados")
                pw.log(f"\n¡Éxito total! Se generaron {len(successful_videos)} paquete(s) ZIP.")
                pw.set_finished(True, f"Se han procesado {len(successful_videos)} vídeo(s) correctamente.", output_dir=output_dir)
            else:
                pw.set_progress(100, "Error en el procesamiento", "Ningún vídeo pudo completarse")
                pw.log("\nNo se pudo completar el procesamiento de los vídeos.")
                pw.set_finished(False, f"Ocurrieron errores en los {len(failed_videos)} vídeos.", output_dir=output_dir)

        except Exception as e:
            pw.log(f"Error fatal: {e}")
            pw.set_finished(False, str(e), output_dir=output_dir)

    pw.start_worker(worker)

if __name__ == "__main__":
    main()
