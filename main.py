import asyncio

import grpc
import file_service_pb2_grpc
from concurrent import futures

from services.grpc_service import FileService
from settings import GRPC_PORT


async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    file_service_pb2_grpc.add_FileServiceServicer_to_server(FileService(), server)
    server.add_insecure_port(f'[::]:{GRPC_PORT}')
    await server.start()
    print(f"gRPC сервер запущен на порту {GRPC_PORT}.")
    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        exit(0)

if __name__ == '__main__':
    asyncio.run(serve())