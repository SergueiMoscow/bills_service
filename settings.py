import os
from environs import Env

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
env = Env()
env.read_env(os.path.join(BASE_DIR, '.env'))

ACCESS_TOKEN = env('ACCESS_TOKEN')
GRPC_PORT = env.int('GRPC_PORT')
RECEIVED_FILES_PATH=env('RECEIVED_FILES_PATH')

PROVERKACHEKA_URL=env('PROVERKACHEKA_URL')
PROVERKACHEKA_TOKEN=env('PROVERKACHEKA_TOKEN')

DB_DSN=env('DB_DSN')
DATABASE_SCHEMA=env('DATABASE_SCHEMA')
