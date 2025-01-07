from convert.extract_data import ExtractData
from convert.pdf_convert import extract_text_from_pdf
from tests.convert.test_pdf import PATH, EXT
from utils.utils import get_files_by_extension


def test_extract_data():
    files_list = get_files_by_extension(PATH, EXT)
    for file_path in files_list:
        text = extract_text_from_pdf(file_path)

        extracted_data = ExtractData(text).process()
        print(extracted_data)
