import os

from services.extract_data import ExtractData
from settings import BASE_DIR


def test_extract_from_txt():
    """
    Extracts from converted pdf->txt file
    :return:
    """
    file = os.path.join(BASE_DIR, 'tests', 'fixtures', 'tin_01.txt')
    with open(file, 'r') as f:
        text = f.read()
    extracted_data = ExtractData(text).process()
    assert extracted_data['date'] == '2025-01-01 01:02'
    assert extracted_data['recipient'] == 'Пётр П.'
    assert extracted_data['sender'] == 'Иван Пупкин'
    assert extracted_data['amount'] == 1000
    assert extracted_data['commission'] == 0
