from datetime import datetime, timedelta

import pytest

from db.connector import AsyncSession
from repository.get_cheques_repository import get_cheques
from schemas.cheque_schemas import ChequeFilterSchema


@pytest.mark.usefixtures('apply_migrations')
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filter_data, expected_cheques_count",
    [
        # базовые тесты
        (ChequeFilterSchema(
            start_date=datetime.now() - timedelta(days=1),
            end_date=datetime.now() + timedelta(days=1)
        ), 1),
        # Ожидаем 1 чек с фильтром по продавцу
        (ChequeFilterSchema(
            seller="Some Seller"
        ), 1),
        # Ожидаем 1 чек с суммой меньше 100
        (ChequeFilterSchema(
            total_op="<",
            total_value=100.0
        ), 1),
        # Без фильтров, ожидаем 2 чека
        (ChequeFilterSchema(), 2),
        # Проверяем равно
        (ChequeFilterSchema(
            total_op="=",
            total_value=180.0
        ), 1),
        # Поиск по заметкам
        (ChequeFilterSchema(
            notes="another"
        ), 1),
        # Ничего не найдено
        (ChequeFilterSchema(
            notes="Non-existent note"
        ), 0),
        # Без фильтров, когда нет чеков
        (ChequeFilterSchema(), 2),
        (ChequeFilterSchema(
            search="test"
        ), 2),
        (ChequeFilterSchema(
            search="Another"
        ), 1),
        (ChequeFilterSchema(
            search="ome Selle"
        ), 1),
        (ChequeFilterSchema(
            search="Non-existent search"
        ), 0),

    ]
)
async def test_get_cheques(faker, cheque_creator, filter_data, expected_cheques_count):
    # Создание чеков
    cheque_creator(
        purchase_date=datetime.now(),
        seller="Some Seller",
        notes="This is a test",
        total=180,
        commit=True
    )
    cheque_creator(
        purchase_date=datetime.now() - timedelta(days=2),
        seller="Other Seller",
        notes="Another test",
        total=50,
        commit=True
    )

    # filter_obj = ChequeFilter(**filter_data)

    async with AsyncSession() as session:
        cheques = await get_cheques(session, filter_data)

    assert len(cheques) == expected_cheques_count


@pytest.mark.usefixtures('apply_migrations')
@pytest.mark.asyncio
async def test_get_cheques_sorting(cheque_creator):
    """
    Тестирование сортировки чеков по дате покупки в порядке возрастания.
    """
    # Устанавливаем базовую дату
    base_date = datetime(2024, 12, 1)

    # Создаём чеки с разными датами покупки
    cheque1 = cheque_creator(purchase_date=base_date + timedelta(days=2), commit=True)  # 3 января
    cheque2 = cheque_creator(purchase_date=base_date + timedelta(days=1), commit=True)  # 2 января
    cheque3 = cheque_creator(purchase_date=base_date + timedelta(days=3), commit=True)  # 4 января

    async with AsyncSession() as session:
        cheques = await get_cheques(session, ChequeFilterSchema())

    purchase_dates = [cheque.purchase_date for cheque in cheques]

    # Проверяем, что даты отсортированы в порядке возрастания
    assert purchase_dates == sorted(purchase_dates), "Чеки не отсортированы по дате покупки в порядке возрастания"

    assert cheques[0].purchase_date == cheque2.purchase_date, "Первый чек должен иметь самую раннюю дату покупки"
    assert cheques[1].purchase_date == cheque1.purchase_date, "Второй чек должен иметь среднюю дату покупки"
    assert cheques[2].purchase_date == cheque3.purchase_date, "Третий чек должен иметь самую позднюю дату покупки"


@pytest.mark.parametrize(
    "filter_data, expected_cheques_count",
    [
        # базовые тесты
        (ChequeFilterSchema(
            start_date=datetime.now() - timedelta(days=5),
            end_date=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
        ), 2),
    ]
)
@pytest.mark.usefixtures('apply_migrations')
@pytest.mark.asyncio
async def test_get_cheques_date_today(cheque_creator, filter_data, expected_cheques_count):
    cheque_creator(
        purchase_date=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
        seller="Some Seller",
        notes="This is a test",
        total=180,
        commit=True
    )
    cheque_creator(
        purchase_date=datetime.now() - timedelta(days=5),
        seller="Other Seller",
        notes="Another test",
        total=50,
        commit=True
    )

    # filter_obj = ChequeFilter(**filter_data)

    async with AsyncSession() as session:
        cheques = await get_cheques(session, filter_data)

    assert len(cheques) == expected_cheques_count
