import grpc
import file_service_pb2_grpc
from concurrent import futures

from services.grpc_service import FileService
from settings import GRPC_PORT


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    file_service_pb2_grpc.add_FileServiceServicer_to_server(FileService(), server)
    server.add_insecure_port(f'[::]:{GRPC_PORT}')
    server.start()
    print(f"gRPC сервер запущен на порту {GRPC_PORT}.")
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        exit(0)

if __name__ == '__main__':
    serve()