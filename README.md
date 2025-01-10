Регенерация gRPC:

`python -m grpc_tools.protoc -I./proto --python_out=./generated/file_service --grpc_python_out=./generated/file_service ./proto/file_service.proto`

`python -m grpc_tools.protoc -I./proto --python_out=./generated/cheques_service --grpc_python_out=./generated/cheques_service ./proto/cheques_service.proto`

В сгенерированных файлах заменить импорт:

для `generated/cheques_service_pb2_grpc.py`:  
`import cheques_service_pb2 as cheques__service__pb2` заменить на  
`from . import cheques_service_pb2 as cheques__service__pb2`

для `generated/file_service_pb2_grpc.py`:  
`import cheques_service_pb2 as cheques__service__pb2` заменить на  
`from . import cheques_service_pb2 as cheques__service__pb2`
