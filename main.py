import os
import sys

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

def main():
    print("========================================")
    print("   Video to Markdown Converter (Desktop)")
    print("========================================")
    
    # 1. Select Input Source
    print("\nSelect Input Method:")
    print("1. YouTube URL")
    print("2. Local File(s)")
    print("3. Local Directory")
    
    # Simple console input for main menu is often faster/cleaner than a popup just for "1, 2, or 3"
    # But let's keep it consistent? No, console is fine for the menu.
    choice = input("Enter 1, 2, or 3: ").strip()


    sources = []
    process_playlist = False

    if choice == '1':
        url = UISelector.get_youtube_url()
        if not url:
            print("No URL entered. Exiting.")
            return

        if "list=" in url:
            # Use GUI for the Yes/No question too
            if UISelector.ask_yes_no("Playlist Detected", "Process entire playlist?"):
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
            return
            
    else:
        print("Invalid choice. Exiting.")
        return

    # 2. Init Modules
    input_handler = InputHandler(output_dir="downloads")
    transcriber = Transcriber(model_size="small")
    frame_extractor = FrameExtractor(output_folder="frames")
    markdown_gen = MarkdownGenerator()

    # 3. Processing Loop
    print("\n--- step 1: Processing Inputs ---")
    video_files = input_handler.process_input(sources, process_playlist=process_playlist)

    if not video_files:
        print("No videos found to process.")
        return

    for i, video_path in enumerate(video_files):
        print(f"\n[{i+1}/{len(video_files)}] Processing: {video_path}")
        try:
            # Convert
            mp4_path = VideoConverter.ensure_mp4(video_path)
            video_title = os.path.splitext(os.path.basename(mp4_path))[0]
            
            # Audio
            audio_path = AudioExtractor.extract_audio(mp4_path)
            if not audio_path: continue
            
            # Transcribe
            transcription_result = transcriber.transcribe(audio_path)
            srt_path = f"{video_title}.srt"
            transcriber.save_srt(transcription_result['segments'], srt_path)
            
            # Smart Frames
            # Note: We might want to clear frames folder or use unique one per video.
            # Current FrameExtractor cleans output_folder on init. 
            # So subsequent videos would overwrite frames if they share the folder? 
            # YES. We must zip immediately OR use unique folders.
            # Fix: Zip immediately after generation.
            
            slides = frame_extractor.extract_frames(mp4_path)
            
            # Markdown
            md_path = markdown_gen.generate_md(video_title, transcription_result['segments'], slides)
            
            # Package
            files_to_zip = [mp4_path, audio_path, srt_path, md_path]
            zip_name = f"{video_title}_package.zip"
            Packager.create_package(zip_name, files_to_include=files_to_zip, folder_to_include="frames")
            
            print(f"SUCCESS: {zip_name}")
            
            # --- Cleanup Intermediate Files ---
            print("--- Step 7: Cleaning Up ---")
            for f in [audio_path, srt_path, md_path]:
                if os.path.exists(f):
                    os.remove(f)
                    print(f"Deleted temporary file: {f}")
            
            # Optionally clean up the frames folder if you don't want it lingering
            import shutil
            if os.path.exists("frames"):
                shutil.rmtree("frames")
                print("Deleted temporary folder: frames")

            
        except Exception as e:
            print(f"ERROR processing {video_path}: {e}")
            import traceback
            traceback.print_exc()

    print("\nAll tasks completed.")

if __name__ == "__main__":
    main()
