import os
import subprocess

class VideoConverter:
    """
    Standardizes video formats to MP4 to ensure compatibility with OpenCV and Whisper.
    """

    @staticmethod
    def ensure_mp4(video_path: str) -> str:
        """
        Checks if file is MP4. If not, converts it.
        Returns the path to the MP4 file (original or new).
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")

        base, ext = os.path.splitext(video_path)
        if ext.lower() == '.mp4':
            return video_path
        
        output_path = f"{base}.mp4"
        print(f"Converting {ext} to .mp4: {output_path}")

        # ffmpeg command to convert to h264/aac mp4
        # -y overwrites output
        ffmpeg_exe = os.environ.get('FFMPEG_PATH', 'ffmpeg')
        cmd = [
            ffmpeg_exe, '-i', video_path,
            '-c:v', 'libx264', '-crf', '23', '-preset', 'medium',
            '-c:a', 'aac', '-b:a', '128k',
            '-y', output_path
        ]

        extra_kwargs = {}
        if os.name == 'nt':
            extra_kwargs['creationflags'] = getattr(subprocess, 'CREATE_NO_WINDOW', 0x08000000)

        try:
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **extra_kwargs)
            print(f"Conversion successful: {output_path}")
            return output_path
        except subprocess.CalledProcessError as e:
            print(f"Error during conversion: {e.stderr.decode()}")
            # Fallback: return original if conversion fails, let downstream try to handle it
            return video_path
