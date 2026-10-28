import subprocess
import os

class AudioExtractor:
    """
    Extracts audio track from video file relative to the video path or to a specific output.
    """

    @staticmethod
    def extract_audio(video_path: str, output_path: str = None) -> str:
        """
        Extracts audio from video_path.
        If output_path is None, saves as 'audio.mp3' in same directory as video.
        Returns path to the extracted audio file.
        """
        if not output_path:
            base, _ = os.path.splitext(video_path)
            output_path = f"{base}.mp3"

        if os.path.exists(output_path):
            os.remove(output_path)  # Force overwrite to ensure fresh extraction

        if not os.path.exists(video_path):
            print(f"Video file not found: {video_path}")
            return None

        print(f"Extracting audio to: {output_path}")

        # Allow overriding ffmpeg executable via environment variable FFMPEG_PATH or ensure_ffmpeg
        ffmpeg_exe = os.environ.get('FFMPEG_PATH')
        if not ffmpeg_exe or not (os.path.isabs(ffmpeg_exe) and os.path.exists(ffmpeg_exe)):
            import shutil
            if not shutil.which('ffmpeg'):
                from src.ffmpeg_installer import ensure_ffmpeg
                ffmpeg_exe = ensure_ffmpeg() or 'ffmpeg'
            else:
                ffmpeg_exe = 'ffmpeg'

        # ffmpeg command: -q:a 0 (best quality VBR), -map a (audio stream only)
        cmd = [
            ffmpeg_exe, '-i', video_path,
            '-q:a', '0', '-map', 'a',
            '-y', output_path
        ]

        extra_kwargs = {}
        if os.name == 'nt':
            extra_kwargs['creationflags'] = getattr(subprocess, 'CREATE_NO_WINDOW', 0x08000000)

        try:
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **extra_kwargs)
            print(f"Audio extraction successful: {output_path}")
            return output_path
        except FileNotFoundError:
            print(
                f"ffmpeg executable not found: '{ffmpeg_exe}'.\n"
                "Please install ffmpeg and ensure it's on your PATH, or set the FFMPEG_PATH environment variable to the ffmpeg executable."
            )
            return None
        except subprocess.CalledProcessError as e:
            stderr = e.stderr.decode() if e.stderr else str(e)
            print(f"Audio extraction failed: {stderr}")
            return None
