import os
from PIL import Image
from pypdf import PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
import typer
from typing import IO, Annotated
from pathlib import Path
from rich import print


def convert_jpg_to_pdf(jpg_path):
    image = Image.open(jpg_path).convert('RGB')
    pdf_bytes = io.BytesIO()
    image.save(pdf_bytes, format='PDF')
    pdf_bytes.seek(0)
    return pdf_bytes

def merge_pdfs(pdf_list, output_path):
    merger = PdfWriter()
    for pdf_file in pdf_list:
        merger.append(pdf_file)
    merger.write(output_path)
    merger.close()

def combine_files_from_folder_to_stream(source: Path, target: Path | IO[any]):
    """
    Combine JPG, PDF files from source folder into one PDF target stream or file path.
    """
    files = sorted(os.listdir(source))
    pdf_files = []

    for file in files:
        file_path = os.path.join(source, file)
        if any(file.lower().endswith(t) for t in {'.jpeg', '.jpg', '.png'}):
            pdf_bytes = convert_jpg_to_pdf(file_path)
            pdf_files.append(pdf_bytes)
        elif file.lower().endswith('.pdf'):
            pdf_files.append(file_path)
        else:
            print(f"[blue]Skipped[/] '{file_path}'")
            continue
        print(f"[yellow]Appended[/] '{file_path}'")

    merge_pdfs(pdf_files, target)
    

def combine_files_from_folder(
    source: Annotated[Path, typer.Argument(help="Path to the source folder")],
    target: Annotated[Path, typer.Argument(help="Target PDF file to create")],
):
    """
    Combine JPG, PNG, PDF files from source folder into one PDF target file.
    """
    combine_files_from_folder_to_stream(source=source, target=target)
    print(f"[yellow]Combined PDF created successfully at[/] '{target}'")
    

def main():
    typer.run(combine_files_from_folder)

if __name__ == "__main__":
    main()

