import os

import grpc

from generated.file_service import file_service_pb2, file_service_pb2_grpc
from services.process_received_data import process_received_data
from settings import ACCESS_TOKEN, RECEIVED_FILES_PATH
import logging

logger = logging.getLogger(__name__)

class FileService(file_service_pb2_grpc.FileServiceServicer):

    async def UploadFile(
        self,
        request,
        context,
    ):
        # Проверяем токен
        if request.token != ACCESS_TOKEN:
            logger.error('Received wrong token')
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('Invalid token')
            return None

        # Сохраняем файл
        file_path = os.path.join(RECEIVED_FILES_PATH, request.filename)  # Укажите желаемое имя файла
        os.makedirs(RECEIVED_FILES_PATH, exist_ok=True)

        with open(file_path, 'wb') as f:
            f.write(request.file)

        # Обработка файла
        # asyncio.run(process_received_data(request, file_path))
        result = await process_received_data(request, file_path)


        logger.info(f'Received {request.filename} / {request.description} from {request.username} ({request.user_id})')
        # return file_service_pb2.UploadFileResponse(message=f"Файл успешно загружен для пользователя {request.username}.")
        return file_service_pb2.UploadFileResponse(message=result)
