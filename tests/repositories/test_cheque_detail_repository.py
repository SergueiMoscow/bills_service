from db.connector import AsyncSession
from db.models import ChequeDetail, Cheque
from repository.cheque_detail_repository import get_cheque_details
from schemas.cheque_schemas import ChequeDetailsFilter
from tests.conftest import cheque_detail_creator

import pytest
from datetime import datetime, timedelta, UTC


@pytest.mark.usefixtures('apply_migrations')
@pytest.mark.asyncio
async def test_check_fixtures(cheque_creator, cheque_detail_creator):
    cheque = cheque_creator(item_count=0, commit=True)
    cheque_detail = cheque_detail_creator(cheque_id=cheque.id, commit=True)
    assert isinstance(cheque, Cheque)
    assert isinstance(cheque_detail, ChequeDetail)


@pytest.mark.usefixtures('apply_migrations')
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filters, expected_items_found",
    [
        (ChequeDetailsFilter(
            start_date=datetime.now() - timedelta(days=1),
            end_date=datetime.now() + timedelta(days=1),
        ), 2),

        (ChequeDetailsFilter(
            start_date=datetime.now() - timedelta(days=1),
            seller="Some Seller",
        ), 2),

        (ChequeDetailsFilter(
            total_op='<',
            total_value=200.0,
        ), 2),

        (ChequeDetailsFilter(
            item_name="Test Item",
        ), 1),

        (ChequeDetailsFilter(
            item_price_op='>',
            item_price_value=50.0,
        ), 1),

        (ChequeDetailsFilter(
            item_price_op='<',
            item_price_value=25.0,
        ), 1),

        (ChequeDetailsFilter(
            item_price_op='>=',
            item_price_value=20.0,
        ), 2),

        (ChequeDetailsFilter(
            total_op='>',
            total_value=200.0,
        ), 0),  # Проверка, что ничего нет

        (ChequeDetailsFilter(
            total_op='=',
            total_value=180.0,
        ), 2),  # Проверка на эквивалентность сумме

        (ChequeDetailsFilter(
            notes="test",
        ), 2),  # Поиск по заметкам

        (ChequeDetailsFilter(
            notes="Non-existent note",
        ), 0),  # Ничего не найдется

        (ChequeDetailsFilter(), 2)  # никаких фильтров, ожидаем 2
    ]
)
async def test_get_cheque_details(faker, cheque_creator, cheque_detail_creator, filters, expected_items_found):
    # Создание чека и деталей
    cheque = cheque_creator(
        purchase_date=datetime.now(),
        seller="Some Seller",
        notes="This is a test",
        item_count=0,
        total=180,
        commit=True
    )
    cheque_detail_creator(cheque_id=cheque.id, name='Test Item', price=20.0, quantity=1, commit=True)
    cheque_detail_creator(cheque_id=cheque.id, name='Another Item', price=80.0, quantity=2, commit=True)

    async with AsyncSession() as session:
        cheque_details = await get_cheque_details(session, filters)

    assert len(cheque_details) == expected_items_found
