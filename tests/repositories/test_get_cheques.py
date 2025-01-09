from datetime import datetime, timedelta

import pytest

from db.connector import AsyncSession
from repository.get_cheques_repository import get_cheques


@pytest.mark.usefixtures('apply_migrations')
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "start_date, end_date, seller, notes, total_op, total_value, expected_cheques_count",
    [
        # базовые тесты
        (datetime.now() - timedelta(days=1), datetime.now() + timedelta(days=1), None, None, None, None, 1),
        # Ожидаем 2 чека
        (datetime.now() - timedelta(days=1), None, "Some Seller", None, None, None, 1),  # Фильтр по продавцу
        (None, None, None, None, '<', 100.0, 1),  # Ожидаем 1 чек с суммой меньше 100
        (None, None, None, None, None, None, 2),  # Без фильтров, ожидаем 2 чека
        (None, None, None, None, '=', 180.0, 1),  # Проверяем равно
        (None, None, None, "another", None, None, 1),  # Поиск по заметкам
        (None, None, None, "Non-existent note", None, None, 0),  # Ничего не найдено
        (None, None, None, None, None, None, 2)  # Без фильтров, когда нет чеков
    ]
)
async def test_get_cheques(faker, cheque_creator, start_date, end_date, seller, notes, total_op, total_value,
                           expected_cheques_count):
    # Создание чеков
    cheque1 = cheque_creator(
        purchase_date=datetime.now(),
        seller="Some Seller",
        notes="This is a test",
        total=180,
        commit=True
    )
    cheque2 = cheque_creator(
        purchase_date=datetime.now() - timedelta(days=2),
        seller="Other Seller",
        notes="Another test",
        total=50,
        commit=True
    )

    async with AsyncSession() as session:
        cheques = await get_cheques(
            session, start_date, end_date, seller, notes,
            total_op, total_value
        )

    assert len(cheques) == expected_cheques_count