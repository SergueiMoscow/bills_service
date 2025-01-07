# PyMuPDF
# pdfplumber
# PyPDF2
import os

from convert.pdf_convert import extract_text_from_pdf
from utils.utils import get_files_by_extension
PATH = '../pdf_fixtures'
EXT = 'pdf'

def test_extract_text_from_pdf(tmp_file):
    files_list = get_files_by_extension(PATH, EXT)
    for file_path in files_list:
        extract_text_from_pdf(file_path, tmp_file)
        assert os.path.exists(tmp_file)
