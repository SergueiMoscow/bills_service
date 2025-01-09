import asyncio
import logging

import grpc
import file_service_pb2_grpc
from concurrent import futures

from services.grpc_service import FileService
from common.settings import GRPC_PORT
from common.logger import setup_logging

setup_logging()

logger = logging.getLogger(__name__)

async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    file_service_pb2_grpc.add_FileServiceServicer_to_server(FileService(), server)
    server.add_insecure_port(f'[::]:{GRPC_PORT}')
    await server.start()
    logger.info(f"gRPC сервер запущен на порту {GRPC_PORT}.")
    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        exit(0)

if __name__ == '__main__':
    asyncio.run(serve())