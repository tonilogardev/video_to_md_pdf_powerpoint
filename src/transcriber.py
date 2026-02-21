import whisper
import torch
import os
from datetime import timedelta
from typing import List, Dict, Any

class Transcriber:
    """
    Wraps OpenAI Whisper model for transcription.
    """

    def __init__(self, model_size="small"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Loading Whisper model ({model_size}) on {self.device}...")
        self.model = whisper.load_model(model_size, device=self.device)
        print("Whisper model loaded.")

    def transcribe(self, audio_path: str) -> Dict[str, Any]:
        """
        Transcribes the audio file.
        Returns the raw result dictionary from Whisper (contains 'segments', 'text', 'language').
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        print(f"Transcribing {audio_path}...")
        result = self.model.transcribe(audio_path)
        return result

    def save_srt(self, segments: List[Dict], output_path: str):
        """
        Formats Whisper segments into standard SRT format and saves to file.
        """
        def format_srt_time(seconds):
            td = timedelta(seconds=seconds)
            total_sec = int(seconds)
            milli = int((seconds - total_sec) * 1000)
            hours = total_sec // 3600
            minutes = (total_sec % 3600) // 60
            secs = total_sec % 60
            return f"{hours:02d}:{minutes:02d}:{secs:02d},{milli:03d}"

        with open(output_path, 'w', encoding='utf-8') as f:
            for i, segment in enumerate(segments):
                start = format_srt_time(segment['start'])
                end = format_srt_time(segment['end'])
                text = segment['text'].strip()

                f.write(f"{i+1}\n")
                f.write(f"{start} --> {end}\n")
                f.write(f"{text}\n\n")
        
        print(f"SRT saved to: {output_path}")
