from db.connector import AsyncSession
from db.models import ChequeDetail, Cheque
from repository.cheque_detail_repository import get_cheque_details
from tests.conftest import cheque_detail_creator

import pytest
from datetime import datetime, timedelta, UTC


@pytest.mark.usefixtures('apply_migrations')
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "start_date, end_date, seller, notes, total_op, total_value, item_name, item_price_op, item_price_value, item_total_op, item_total_value, expected_items_found",
    [
        # базовые тесты
        (datetime.now() - timedelta(days=1), datetime.now() + timedelta(days=1), None, None, None, None, None, None, None, None, None, 2),
        (datetime.now() - timedelta(days=1), None, "Some Seller", None, None, None, None, None, None, None, None, 2),
        (None, None, None, None, '<', 200.0, None, None, None, None, None, 2),
        (None, None, None, None, None, None, "Test Item", None, None, None, None, 1),
        (None, None, None, None, None, None, None, '>', 50.0, None, None, 1),
        # # тесты по цене товара
        (None, None, None, None, None, None, None, '<', 25.0, None, None, 1),
        (None, None, None, None, None, None, None, '>=', 20.0, None, None, 2),
        # тесты по общей сумме чека
        (None, None, None, None, '>', 200.0, None, None, None, None, None, 0),  # Проверка, что ничего нет
        (None, None, None, None, '=', 180.0, None, None, None, None, None, 2),  # Проверка на эквивалентность сумме
        # тесты по заметкам
        (None, None, None, "test", None, None, None, None, None, None, None, 2),  # Поиск по заметкам
        (None, None, None, "Non-existent note", None, None, None, None, None, None, None, 0),  # Ничего не найдется
        # # тесты с пустыми значениями
        (None, None, None, None, None, None, None, None, None, None, None, 2)  # никаких фильтров, ожидаем 2
    ]
)

async def test_get_cheque_details(faker, cheque_creator, cheque_detail_creator, start_date, end_date, seller, notes, total_op, total_value, item_name,
                                  item_price_op, item_price_value, item_total_op, item_total_value, expected_items_found):
    # Создание чека и деталей
    cheque = cheque_creator(
        purchase_date=datetime.now(),
        seller="Some Seller",
        notes="This is a test",
        item_count = 0,
        total=180,
        commit=True
    )
    cheque_detail_creator(cheque_id=cheque.id, name='Test Item', price=20.0, quantity=1, commit=True),
    cheque_detail_creator(cheque_id=cheque.id, name='Another Item', price=80.0, quantity=2, commit=True),

    async with AsyncSession() as session:
        cheque_details = await get_cheque_details(
            session, start_date, end_date, seller, notes,
            total_op, total_value, item_name,
            item_price_op, item_price_value, item_total_op, item_total_value
        )

    assert len(cheque_details) == expected_items_found


@pytest.mark.usefixtures('apply_migrations')
@pytest.mark.asyncio
async def test_get_details(cheque_creator, cheque_detail_creator):
    cheque = cheque_creator(item_count=0, commit=True)
    cheque_detail = cheque_detail_creator(cheque_id=cheque.id, commit=True)
    assert isinstance(cheque, Cheque)
    assert isinstance(cheque_detail, ChequeDetail)

