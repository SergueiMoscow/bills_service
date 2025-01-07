import os


def get_files_by_extension(directory_path, extension):
    """
    Получает список файлов с заданным расширением в указанной директории.

    :param directory_path: Путь к директории
    :param extension: Расширение файлов (например, '.pdf')
    :return: Список полных путей к файлам с заданным расширением
    """
    matching_files = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith(extension.lower()):
                full_path = os.path.join(root, file)
                matching_files.append(full_path)
    return matching_files