from datetime import datetime

from services.extract_data import ExtractData
from services.pdf_convert import extract_text_from_pdf
from tests.convert.test_pdf import PATH, EXT
from utils.utils import get_files_by_extension
import logging


logger = logging.getLogger(__name__)


def test_extract_from_txt():
    """
    Extracts from converted pdf->txt file
    :return:
    """
    file = '../fixtures/sber_from_pdf.txt'
    with open(file, 'r') as f:
        text = f.read()
    extracted_data = ExtractData(text).process()
    assert extracted_data['date'] == '2025-01-04 12:26'
    assert extracted_data['recipient'] == 'OOO ORGANIZATION City RUS'
    assert extracted_data['sender'] == 'Иван Иванович И.'
    assert extracted_data['amount'] == 15000
    assert extracted_data['commission'] == 0
    assert '1234' in extracted_data['account']