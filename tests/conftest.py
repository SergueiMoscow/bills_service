import json

import pytest
import tempfile
import os
from datetime import datetime
from alembic import command

import settings
from db.connector import Session
from db.models import ChequeDetail, Cheque
from services.grpc_service import FileService
from settings import BASE_DIR
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


@pytest.fixture
def cheque_detail_creator_old(faker):
    def _create(
        cheque_id: int,
        name: str | None = None,
        price: float | None = None,
        quantity: float | None = None,
        commit: bool = True,
    ):
        if name is None:
            name = faker.word()
        if price is None:
            price = round(faker.random.uniform(1.0, 10000.0), 2)
        if quantity is None:
            quantity = faker.random.randint(1, 10)
        cheque_detail = ChequeDetail(
            cheque_id=cheque_id,
            name=name,
            price=price,
            quantity=quantity,
            total=price*quantity,
        )
        if commit:
            with Session() as session:
                session.add(cheque_detail)
                session.commit()
        return cheque_detail
    return _create


@pytest.fixture
def cheque_creator_old(faker, cheque_detail_creator):
    def _create(
        user: str | None = None,
        file_name: str | None = None,
        purchase_date: datetime | None = None,
        seller: str | None = None,
        account: str | None = None,
        total: float = 0,
        notes: str | None = None,
        item_count: int | None = None,
        commit: bool = True,
    ):
        if file_name is None:
            file_name = faker.word()
        if purchase_date is None:
            purchase_date = faker.date_time()
        if user is None:
            user = faker.word()
        if seller is None:
            seller = faker.word()
        if account is None:
            account = faker.word()
        if total is None:
            total = faker.random.randint(1, 10000)
        if notes is None:
            notes = faker.word()
        if item_count is None:
            item_count = faker.random.randint(1, 5)


        cheque = Cheque(
            user=user,
            file_name=file_name,
            purchase_date=purchase_date,
            seller=seller,
            account=account,
            total=total,
            notes=notes,
        )

        if commit:
            with Session() as session:
                session.add(cheque)
                session.commit()

        cheque_details = []

        for _ in range(item_count):
            detail = cheque_detail_creator(
                cheque_id=cheque.id,
                commit=False
            )  # Предполагаем, что cheque_detail_creator принимает cheque
            cheque_details.append(detail)

        if commit:
            with Session() as session:
                for detail in cheque_details:
                    detail.cheque_id = cheque.id  # Связываем деталь с чеком
                    session.add(detail)
                session.commit()
        return cheque
    return _create


@pytest.fixture
def cheque_detail_creator(faker):
    def _create(
            cheque_id: int,
            name: str | None = None,
            price: float | None = None,
            quantity: float | None = None,
            commit: bool = True,
    ):
        if name is None:
            name = faker.word()
        if price is None:
            price = round(faker.random.uniform(1.0, 10000.0), 2)
        if quantity is None:
            quantity = faker.random.randint(1, 10)

        cheque_detail = ChequeDetail(
            cheque_id=cheque_id,
            name=name,
            price=price,
            quantity=quantity,
            total=price * quantity,
        )

        if commit:
            with Session() as session:
                session.add(cheque_detail)
                session.commit()

        return cheque_detail

    return _create


@pytest.fixture
def cheque_creator(faker, cheque_detail_creator):
    def _create(
            user: str | None = None,
            file_name: str | None = None,
            purchase_date: datetime | None = None,
            seller: str | None = None,
            account: str | None = None,
            total: float = 0,
            notes: str | None = None,
            item_count: int | None = None,
            commit: bool = True,
    ):
        if file_name is None:
            file_name = faker.word()
        if purchase_date is None:
            purchase_date = faker.date_time()
        if user is None:
            user = faker.word()
        if seller is None:
            seller = faker.word()
        if account is None:
            account = faker.word()
        if total <= 0:
            total = round(faker.random.uniform(1.0, 10000.0), 2)
        if notes is None:
            notes = faker.word()
        if item_count is None:
            item_count = faker.random.randint(1, 5)

        cheque = Cheque(
            user=user,
            file_name=file_name,
            purchase_date=purchase_date,
            seller=seller,
            account=account,
            total=total,
            notes=notes,
        )

        cheque_details = []

        for _ in range(item_count):
            detail = cheque_detail_creator(cheque_id=cheque.id, commit=False)
            cheque_details.append(detail)
            cheque.details.append(detail)  # Сохраняем детали в объекте Cheque

        if commit:
            with Session() as session:
                session.add(cheque)
                session.flush()

                for detail in cheque_details:
                    detail.cheque_id = cheque.id  # Связываем детали с чеком
                    session.add(detail)

                for detail in cheque_details:
                    detail.cheque_id = cheque.id
                    session.add(detail)

                session.commit()  # Коммитируем все детали

        return cheque

    return _create

@pytest.fixture
def created_cheque():
    ...