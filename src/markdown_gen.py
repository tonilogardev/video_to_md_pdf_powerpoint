import os

class MarkdownGenerator:
    """
    Assembles the final Markdown document from transcription segments and extracted frames.
    """

    @staticmethod
    def generate_md(video_title: str, segments: list, slides: list, output_path: str = None):
        """
        video_title: Name of the video
        segments: List of dicts from Whisper {'start': 0.0, 'end': 5.0, 'text': '...'}
        slides: List of dicts from FrameExtractor {'time_sec': 12.0, 'path': '...', 'timestamp': '00:12'}
        """
        if not output_path:
            output_path = f"{video_title}.md"

        print(f"Generating Markdown: {output_path}")

        md_content = []
        md_content.append(f"# {video_title}\n")
        md_content.append(f"**Generated Notes from Video**\n")
        md_content.append("---\n\n")

        # We need to interleave text and images based on timestamps.
        # Strategy: Iterate through slides. For each slide, find all text that occurs 
        # AFTER this slide appeared but BEFORE the next slide appears.
        
        # 1. Sort everything just in case
        slides.sort(key=lambda x: x['time_sec'])
        # segments are usually sorted by Whisper

        current_segment_idx = 0
        total_segments = len(segments)

        for i, slide in enumerate(slides):
            # Header for the slide
            slide_time = slide['time_sec']
            timestamp_str = slide['timestamp']
            image_rel_path = slide['path']  # Assuming path is relative or will be zipped relative
            
            # Add the Image
            md_content.append(f"## Timestamp: {timestamp_str}\n")
            md_content.append(f"![Slide {timestamp_str}]({image_rel_path})\n\n")
            
            # Determine end time for this section (it's the next slide's time, or end of video)
            next_slide_time = slides[i+1]['time_sec'] if (i + 1) < len(slides) else 999999.0
            
            # Collect text segments that fall into this window [slide_time, next_slide_time)
            # Special case: Include segments that started slightly before this slide if they weren't covered yet?
            # Simplification: Just check start times.
            
            section_text = []
            while current_segment_idx < total_segments:
                seg = segments[current_segment_idx]
                if seg['start'] < next_slide_time:
                    # This segment belongs to the current or previous block. 
                    # If it's already past the current slide start, it definitely belongs here.
                    # If it started slightly before, it might have been missed by previous loop? 
                    # No, because current_segment_idx increments.
                    section_text.append(seg['text'].strip())
                    current_segment_idx += 1
                else:
                    # Segment starts after the next slide, so we stop here
                    break
            
            if section_text:
                md_content.append(f"**Transcript:**\n")
                md_content.append("> " + " ".join(section_text) + "\n\n")
            else:
                md_content.append("*(No speech detected in this section)*\n\n")
            
            md_content.append("---\n")

        # Catch any remaining text after last slide
        if current_segment_idx < total_segments:
             md_content.append("## Ending Transcript\n")
             remaining_text = [seg['text'].strip() for seg in segments[current_segment_idx:]]
             md_content.append("> " + " ".join(remaining_text) + "\n\n")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("".join(md_content))
        
        print(f"Markdown Generation Complete: {output_path}")
        return output_path
