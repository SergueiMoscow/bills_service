import json

import pytest
import tempfile
import os

from alembic import command

from common import settings
from db.connector import Session
from services.grpc_service import FileService
from common.settings import BASE_DIR
from sqlalchemy import text as sa_text
from alembic.config import Config


@pytest.fixture
def apply_migrations():
    assert 'TEST' in settings.DATABASE_SCHEMA.upper(), 'Попытка использовать не тестовую схему.'
    alembic_ini = os.path.join(BASE_DIR, 'alembic.ini')

    with Session() as session:
        session.execute(sa_text(f'CREATE SCHEMA IF NOT EXISTS {settings.DATABASE_SCHEMA};'))
        session.commit()

    alembic_cfg = Config(alembic_ini)
    alembic_cfg.set_main_option('script_location', os.path.join(BASE_DIR, 'migrations'))
    command.downgrade(alembic_cfg, 'base')
    command.upgrade(alembic_cfg, 'head')

    yield command, alembic_cfg

    command.downgrade(alembic_cfg, 'base')

    with Session() as session:
        if 'TEST' in settings.DATABASE_SCHEMA.upper():
            session.execute(sa_text(f'DROP SCHEMA IF EXISTS {settings.DATABASE_SCHEMA} CASCADE;'))
            session.commit()
        else:
            raise Exception('Использование не тестовой схемы')



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


@pytest.fixture
def json_fixture():
    json_file_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'json_fixture.json')
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    return data
