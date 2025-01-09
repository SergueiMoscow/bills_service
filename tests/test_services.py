import os
import file_service_pb2
from unittest.mock import MagicMock

from settings import ACCESS_TOKEN, RECEIVED_FILES_PATH

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
RECEIVED_FILES_PATH = os.path.abspath(RECEIVED_FILES_PATH)


def test_upload_file(file_service):
    request = file_service_pb2.UploadFileRequest(
        file=b"sample file content",
        user_id="123",
        username="test_user",
        description="Test file",
        filename="test_file.txt",
        token=ACCESS_TOKEN,
    )

    context = MagicMock()
    response = file_service.UploadFile(request, context)
    assert response.message == "Файл успешно загружен для пользователя test_user."
    assert os.path.exists(os.path.join(RECEIVED_FILES_PATH, "test_file.txt"))
    os.remove(os.path.join(RECEIVED_FILES_PATH, "test_file.txt"))