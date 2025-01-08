import os

import requests


def download_content_from_url(url, save_as=None):
    """
    Скачивает содержимое по указанной ссылке и сохраняет в файл, если задано имя файла.

    :param url: URL-адрес для скачивания.
    :param save_as: Имя файла для сохранения содержимого (необязательно).
    :return: Содержимое скачанной страницы в виде байтов.
    :raises: requests.exceptions.RequestException при ошибках сети.
             IOError при ошибках сохранения файла.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        content = response.content

        if save_as:
            os.makedirs(os.path.dirname(save_as), exist_ok=True) if os.path.dirname(save_as) else None
            with open(save_as, 'wb') as file:
                file.write(content)
            print(f"Содержимое сохранено в файл: {save_as}")

        return content

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при скачивании содержимого: {e}")
        raise
    except IOError as e:
        print(f"Ошибка при сохранении файла: {e}")
        raise
