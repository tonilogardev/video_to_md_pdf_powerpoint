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

        print(f"Extracting audio to: {output_path}")

        # ffmpeg command: -q:a 0 (best quality VBR), -map a (audio stream only)
        cmd = [
            'ffmpeg', '-i', video_path,
            '-q:a', '0', '-map', 'a',
            '-y', output_path
        ]

        try:
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"Audio extraction successful: {output_path}")
            return output_path
        except subprocess.CalledProcessError as e:
            print(f"Audio extraction failed: {e.stderr.decode()}")
            return None
