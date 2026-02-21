import zipfile
import os
from typing import List

class Packager:
    """
    Zips up the final package: Markdown, Frames, Audio, Video, SRT.
    """

    @staticmethod
    def create_package(zip_name: str, files_to_include: List[str], folder_to_include: str = "frames"):
        """
        Creates a zip file containing the specified files and folder.
        """
        if not zip_name.endswith(".zip"):
            zip_name += ".zip"

        print(f"Creating package: {zip_name}...")

        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add individual files
            for file_path in files_to_include:
                if file_path and os.path.exists(file_path):
                    print(f"Adding file: {file_path}")
                    zipf.write(file_path, arcname=os.path.basename(file_path))
                else:
                    print(f"Warning: File not found for zipping: {file_path}")

            # Add folder (frames)
            if folder_to_include and os.path.exists(folder_to_include):
                print(f"Adding folder: {folder_to_include}")
                for root, dirs, files in os.walk(folder_to_include):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # Maintain folder structure within zip
                        # arcname = frames/frame_001.jpg
                        arcname = os.path.join(os.path.basename(folder_to_include), file)
                        zipf.write(file_path, arcname=arcname)
        
        print(f"Package created successfully! Size: {os.path.getsize(zip_name) / (1024*1024):.2f} MB")
        return zip_name
