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

DATABASE_URI=env('DATABASE_URI')
DATABASE_SCHEMA=env('DATABASE_SCHEMA')

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(DATABASE_URI.replace('postgresql:', 'postgresql+asyncpg:'), echo=True)

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False  # Вам, возможно, понадобится этот параметр для асинхронных сессий
)
