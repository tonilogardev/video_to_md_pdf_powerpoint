import os
import sys

try:
    from markdown_pdf import Section, MarkdownPdf
except ImportError:
    print("Error: The 'markdown-pdf' library is required.")
    print("Please install it running: pip install markdown-pdf")
    sys.exit(1)

class PdfGenerator:
    """
    Handles the conversion of the generated Markdown file into a PDF document.
    """

    def __init__(self):
        pass

    def generate_pdf(self, md_path: str, output_pdf_path: str) -> str:
        """
        Reads a Markdown file, processes it (including local images), 
        and saves it as a PDF file.

        Args:
            md_path (str): The path to the source .md file.
            output_pdf_path (str): The desired path for the output .pdf file.

        Returns:
            str: The path to the generated PDF file if successful, otherwise None.
        """
        print(f"Generating PDF from: {md_path}")
        try:
             # Ensure the source file exists
             if not os.path.exists(md_path):
                 print(f"Error: Markdown file '{md_path}' not found.")
                 return None

             # Read the Markdown content
             with open(md_path, 'r', encoding='utf-8') as f:
                 md_content = f.read()

             # Initialize the PDF converter
             pdf = MarkdownPdf(toc_level=2) # Generate Table of Contents based on H2
             
             # Add the markdown content as a section with root directory set to md_path's folder
             md_root = os.path.dirname(os.path.abspath(md_path))
             pdf.add_section(Section(md_content, root=md_root))

             # Ensure the output directory exists
             output_dir = os.path.dirname(output_pdf_path)
             if output_dir and not os.path.exists(output_dir):
                 os.makedirs(output_dir)

             # Save the PDF
             pdf.save(output_pdf_path)
             print(f"PDF successfully generated: {output_pdf_path}")
             return output_pdf_path

        except Exception as e:
             print(f"Failed to generate PDF: {e}")
             import traceback
             traceback.print_exc()
             return None
