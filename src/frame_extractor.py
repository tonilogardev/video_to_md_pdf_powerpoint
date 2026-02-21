import cv2
import os
import shutil
from skimage.metrics import structural_similarity as ssim
from typing import List, Dict, Any

class FrameExtractor:
    """
    Extracts high-quality slides/frames from video using SSIM for deduplication.
    """

    def __init__(self, output_folder="frames"):
        self.output_folder = output_folder

    def _is_duplicate(self, img1, img2, threshold=0.98):
        """
        Compares two images using SSIM. Returns True if they are similar enough to be duplicates.
        """
        # Convert to grayscale for faster comparison
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        
        # Calculate structural similarity
        score, _ = ssim(gray1, gray2, full=True)
        return score > threshold

    def extract_frames(self, video_path: str, sample_interval: int = 2) -> List[Dict[str, Any]]:
        """
        Main extraction loop. 
        sample_interval: Check a frame every N seconds (optimization).
        Returns a list of dicts: {'path': '...', 'time_sec': 12.5, 'timestamp': '00:12'}
        """
        if os.path.exists(self.output_folder):
            shutil.rmtree(self.output_folder)
        os.makedirs(self.output_folder)

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
             print(f"Error opening video: {video_path}")
             return []

        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps
        
        # Calculate how many frames to skip based on sample_interval
        # defaulting to check every 1 second minimum to be safe, or user param
        frames_to_skip = int(fps * sample_interval) 
        if frames_to_skip < 1: frames_to_skip = 1

        kept_slides = []
        last_saved_frame = None
        curr_frame_idx = 0
        last_saved_time = -999

        print(f"Starting frame extraction loop (Total frames: {total_frames}, FPS: {fps:.2f})...")

        while curr_frame_idx < total_frames:
            cap.set(cv2.CAP_PROP_POS_FRAMES, curr_frame_idx)
            ret, frame = cap.read()
            if not ret: break

            time_sec = curr_frame_idx / fps
            is_new = False
            
            # Logic:
            # 1. Always save first frame
            # 2. Save if SSIM shows it's different from last saved
            # 3. Force save if > 60 seconds have passed since last save (Context keeper)

            if last_saved_frame is None:
                is_new = True
            elif (time_sec - last_saved_time) > 60:
                 is_new = True
                 print(f"Forced capture at {time_sec:.2f}s (Time limit reached)")
            else:
                 is_new = not self._is_duplicate(last_saved_frame, frame)

            if is_new:
                # Save it
                # Format: frame_0000.jpg (using raw frame count or timestamp in filename)
                # Using timestamp in filename for easier manual sorting/viewing
                clean_time = int(time_sec)
                hours = clean_time // 3600
                minutes = (clean_time % 3600) // 60
                seconds = clean_time % 60
                
                filename = f"frame_{hours:02d}_{minutes:02d}_{seconds:02d}.jpg"
                path = os.path.join(self.output_folder, filename)
                
                cv2.imwrite(path, frame)
                
                kept_slides.append({
                    'path': path,
                    'time_sec': time_sec,
                    'timestamp': f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                })
                
                last_saved_frame = frame
                last_saved_time = time_sec

            # Jump ahead
            curr_frame_idx += frames_to_skip

        cap.release()
        print(f"Extraction complete. Saved {len(kept_slides)} slides.")
        return kept_slides
