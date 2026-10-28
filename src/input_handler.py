import os
import yt_dlp
from typing import List, Union

class InputHandler:
    """
    Handles input sources: YouTube URLs (single/playlist) or Local File Paths.
    """

    def __init__(self, output_dir="downloads", ffmpeg_location=None):
        self.output_dir = output_dir
        self.ffmpeg_location = ffmpeg_location or os.environ.get('FFMPEG_PATH')
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
        """Downloads video(s) from YouTube using yt-dlp with anti-403 client strategies."""
        ffmpeg_loc = self.ffmpeg_location or os.environ.get('FFMPEG_PATH')
        
        # Strategies to bypass YouTube 403 Forbidden on player API
        strategies = [
            ['android', 'web'],
            ['android'],
            ['mweb', 'android'],
        ]

        last_error = None

        for client_list in strategies:
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best/18/b',
                'outtmpl': os.path.join(self.output_dir, '%(title)s.%(ext)s'),
                'merge_output_format': 'mp4',
                'quiet': False,
                'noplaylist': not process_playlist,
                'http_chunk_size': 10485760,
                'extractor_args': {
                    'youtube': {
                        'player_client': client_list,
                    }
                },
            }

            if ffmpeg_loc:
                ydl_opts['ffmpeg_location'] = ffmpeg_loc

            downloaded_paths = []

            # Hook to capture filename AFTER merging or downloading is complete
            def postprocessor_hook(d):
                if d.get('status') == 'finished':
                    info_dict = d.get('info_dict', {})
                    filepath = info_dict.get('filepath') or d.get('filename')
                    if filepath and filepath not in downloaded_paths:
                        downloaded_paths.append(filepath)

            ydl_opts['postprocessor_hooks'] = [postprocessor_hook]

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    
                    entries = info.get('entries') if info and 'entries' in info else ([info] if info else [])
                    for entry in entries:
                        if not entry:
                            continue
                        
                        for req in entry.get('requested_downloads', []):
                            req_path = req.get('filepath') or req.get('_filename')
                            if req_path and req_path not in downloaded_paths:
                                downloaded_paths.append(req_path)

                        fn = ydl.prepare_filename(entry)
                        if fn not in downloaded_paths:
                            downloaded_paths.append(fn)

                # Normalize and resolve valid paths that actually exist on disk (avoiding duplicates)
                valid_paths = []
                seen_abs = set()
                for p in downloaded_paths:
                    abs_p = os.path.abspath(p)
                    if os.path.exists(abs_p) and abs_p not in seen_abs:
                        seen_abs.add(abs_p)
                        valid_paths.append(p)
                    else:
                        base, _ = os.path.splitext(p)
                        for ext in ('.mp4', '.mkv', '.webm', '.avi'):
                            alt = base + ext
                            alt_abs = os.path.abspath(alt)
                            if os.path.exists(alt_abs) and alt_abs not in seen_abs:
                                seen_abs.add(alt_abs)
                                valid_paths.append(alt)
                                break
                
                if valid_paths:
                    return valid_paths

            except Exception as e:
                last_error = e
                err_msg = str(e)
                if '403' in err_msg or 'Forbidden' in err_msg:
                    print(f"Client {client_list} encountered 403, trying alternate client strategy...")
                    continue
                else:
                    print(f"Error downloading {url}: {e}")
                    break

        if last_error:
            print(f"Failed to download {url} after trying all strategies: {last_error}")
        return []
