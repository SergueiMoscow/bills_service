import os

import pytest

import file_service_pb2
from unittest.mock import MagicMock

from settings import ACCESS_TOKEN, RECEIVED_FILES_PATH

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
RECEIVED_FILES_PATH = os.path.abspath(RECEIVED_FILES_PATH)


@pytest.mark.asyncio
@pytest.mark.usefixtures('apply_migrations')
async def test_upload_file(file_service, mock_get_cheque_from_api_service_ok):
    request = file_service_pb2.UploadFileRequest(
        file=b"sample file content",
        user_id="123",
        username="test_user",
        description="Test file",
        filename="test_file.txt",
        token=ACCESS_TOKEN,
    )

    context = MagicMock()
    response = await file_service.UploadFile(request, context)
    assert response.message == "Cheque added to database"
    assert os.path.exists(os.path.join(RECEIVED_FILES_PATH, "test_file.txt"))
    os.remove(os.path.join(RECEIVED_FILES_PATH, "test_file.txt"))

@pytest.mark.asyncio
@pytest.mark.usefixtures('apply_migrations')
async def test_upload_file_exceeded(file_service, mock_get_cheque_from_api_service_exceeded):
    request = file_service_pb2.UploadFileRequest(
        file=b"sample file content",
        user_id="123",
        username="test_user",
        description="Test file",
        filename="test_file.txt",
        token=ACCESS_TOKEN,
    )

    context = MagicMock()
    response = await file_service.UploadFile(request, context)
    assert response.message == "Превышено количество обращений по чеку."
    assert os.path.exists(os.path.join(RECEIVED_FILES_PATH, "test_file.txt"))
    os.remove(os.path.join(RECEIVED_FILES_PATH, "test_file.txt"))