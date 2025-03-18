from main import combine_files_from_folder_to_stream
from pathlib import Path
from io import BytesIO

def test_happy():
  s = BytesIO()
  combine_files_from_folder_to_stream(source=Path("tests/data/abc"), target=s)
  with open("tests/data/abc.pdf", 'rb') as file:
    assert file.read() == s.getvalue()
