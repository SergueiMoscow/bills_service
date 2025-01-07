import pytest
import tempfile
import os
from services.grpc_service import FileService


@pytest.fixture
def file_service():
    return FileService()

@pytest.fixture
def tmp_file():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
        tmp_file_name = tmp.name
    yield tmp_file_name
    if os.path.exists(tmp_file_name):
        os.remove(tmp_file_name)
