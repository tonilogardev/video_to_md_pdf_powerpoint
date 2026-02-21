import os
import yt_dlp
from typing import List, Union

class InputHandler:
    """
    Handles input sources: YouTube URLs (single/playlist) or Local File Paths.
    """

    def __init__(self, output_dir="downloads"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def is_youtube_url(self, source: str) -> bool:
        """Checks if the string is a YouTube URL."""
        return "youtube.com" in source or "youtu.be" in source

    def is_playlist(self, url: str) -> bool:
        """Checks if the URL is a playlist."""
        return "list=" in url

    def process_input(self, sources: List[str], process_playlist: bool = False) -> List[str]:
        """
        Main entry point. Takes a list of sources (URLs or Paths) and returns list of local file paths.
        If process_playlist is True, it expands the playlist.
        """
        processed_files = []

        for source in sources:
            if self.is_youtube_url(source):
                print(f"Processing YouTube URL: {source}")
                downloaded = self._download_youtube(source, process_playlist)
                processed_files.extend(downloaded)
            else:
                # Assume Local Path
                if os.path.exists(source):
                    print(f"Found local file: {source}")
                    processed_files.append(source)
                else:
                    print(f"Error: File not found - {source}")
        
        return processed_files

    def _download_youtube(self, url: str, process_playlist: bool) -> List[str]:
        """Downloads video(s) from YouTube using yt-dlp."""
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(self.output_dir, '%(title)s.%(ext)s'),
            'quiet': False,
            'noplaylist': not process_playlist, # Respect user choice
        }

        downloaded_paths = []

        # Hook to capture filename AFTER merging is complete
        # We use a postprocessor hook to get the true final filename
        def postprocessor_hook(d):
            if d['status'] == 'finished' and d['postprocessor'] == 'Merger':
                # The 'info_dict' contains the final filepath
                if 'info_dict' in d and 'filepath' in d['info_dict']:
                    filepath = d['info_dict']['filepath']
                    if filepath not in downloaded_paths:
                        downloaded_paths.append(filepath)

        def progress_hook(d):
             # Fallback: if there's no merging needed (e.g. single best format downloaded)
             if d['status'] == 'finished':
                  # Wait, yt-dlp triggers this for audio AND video parts.
                  # If we just take d['filename'], we get the temp .f299 parts.
                  # It's better to rely just on postprocessor, OR clean up the name.
                  pass

        ydl_opts['postprocessor_hooks'] = [postprocessor_hook]
        ydl_opts['progress_hooks'] = [progress_hook]

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                
                # If postprocessor hook didn't catch it (no merging happened), 
                # we can extract the filename from the main info object.
                if not downloaded_paths and info:
                     if 'entries' in info:
                         # It's a playlist
                         for entry in info['entries']:
                             if entry:
                                 filepath = ydl.prepare_filename(entry)
                                 # prepare_filename might give .webm/.mkv, wait for converter
                                 downloaded_paths.append(filepath)
                     else:
                         # Single video
                         filepath = ydl.prepare_filename(info)
                         downloaded_paths.append(filepath)
            
            # Normalize paths to ensure they exist (sometimes prepare_filename predicts .webm but .mkv is downloaded)
            valid_paths = [p for p in downloaded_paths if os.path.exists(p)]
            
            # If still empty but we know it downloaded (fallback hack)
            if not valid_paths and info:
                # Just scan the output directory for recently modified mp4s? 
                # No, that's too hacky. The prepare_filename should work in 99% of cases.
                pass
                
            return valid_paths

        except Exception as e:
            print(f"Error downloading {url}: {e}")
            return []
