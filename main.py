import asyncio
import logging

import grpc

from generated.cheques_service import cheques_service_pb2_grpc
from generated.file_service import file_service_pb2_grpc
from concurrent import futures

from generated.file_service import file_service_pb2_grpc
from services.grpc.cheques_service import ChequesService
from services.grpc.file_service import FileService
from settings import GRPC_PORT
from common.logger import setup_logging

setup_logging()

logger = logging.getLogger(__name__)

async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    file_service_pb2_grpc.add_FileServiceServicer_to_server(FileService(), server)
    cheques_service_pb2_grpc.add_ChequeServiceServicer_to_server(ChequesService(), server)
    server.add_insecure_port(f'[::]:{GRPC_PORT}')
    await server.start()
    logger.info(f"gRPC сервер запущен на порту {GRPC_PORT}.")
    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("gRPC сервер остановлен.")
    except asyncio.exceptions.CancelledError:
        logger.info("gRPC сервер остановлен.")
    finally:
        await server.stop(0)


if __name__ == '__main__':
    try:
        asyncio.run(serve())
    except KeyboardInterrupt:
        logger.info("Программа остановлена пользователем.")