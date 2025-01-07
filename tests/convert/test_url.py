import os

from convert.url_convert import download_content_from_url
from settings import BASE_DIR


def test_download_content_from_url():
    url = 'https://check.yandex.ru/?n=169111&fn=7380440801185382&fpd=3769337301'
    filename = os.path.join(BASE_DIR, 'tests', 'pdf_fixtures', 'bill_from_url.txt')
    download_content_from_url(url, save_as=filename)
    assert os.path.exists(filename)
