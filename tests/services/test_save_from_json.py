import pytest
from sqlalchemy import select

from db.connector import AsyncSession
from db.models import Pattern, Cheque, ChequeDetail
from repository.cheque_repository import save_cheque_from_json


@pytest.mark.usefixtures('apply_migrations')
@pytest.mark.parametrize(
    "pattern_data, json_data, expected_result",
    [
        (
            # Паттерн: для модели Cheque, если поле 'seller' содержит 'ORGANIZATION', установить 'category'='Коммунальные услуги' в ChequeDetail
            {
                "model_in": "Cheque",
                "field_in": "seller",
                "include": "ORGANIZATION",
                "model_out": "ChequeDetail",
                "field_out": "category",
                "value_out": "Коммунальные услуги",
            },
            {
                "data": {
                    "json": {
                        "code": 1,
                        "operationType": "purchase",
                        "totalSum": 15000,  # 150.00
                        "dateTime": "2023-10-01T12:34:56",
                        "user": "ORGANIZATION ABC",
                        "retailPlace": "Some Retail Place",
                        "account": "1234567890",
                        "items": [
                            {
                                "name": "Item A",
                                "price": 5000,  # 50.00
                                "quantity": 1,
                                "sum": 5000,
                            },
                            {
                                "name": "Item B",
                                "price": 10000,  # 100.00
                                "quantity": 1,
                                "sum": 10000,
                            },
                        ],
                    }
                }
            },
            "Коммунальные услуги",
        ),
        (
            # Паттерн не должен примениться, так как 'seller' не содержит 'ORG'
            {
                "model_in": "Cheque",
                "field_in": "seller",
                "include": "ORGANIZATION",
                "model_out": "ChequeDetail",
                "field_out": "category",
                "value_out": "Коммунальные услуги",
            },
            {
                "data": {
                    "json": {
                        "code": 1,
                        "operationType": "purchase",
                        "totalSum": 20000,  # 200.00
                        "dateTime": "2023-10-02T14:20:00",
                        "user": "Individual John",
                        "retailPlace": "Another Retail Place",
                        "account": "0987654321",
                        "items": [
                            {
                                "name": "Item C",
                                "price": 20000,  # 200.00
                                "quantity": 1,
                                "sum": 20000,
                            },
                        ],
                    }
                }
            },
            None,  # Ожидаем, что категория не изменится
        ),
    ],
)
@pytest.mark.asyncio
async def test_save_cheque_from_json(
    pattern_data,
    json_data,
    expected_result,
):
    # Добавляем паттерн в базу данных
    pattern = Pattern(**pattern_data)
    async with AsyncSession() as session:
        session.add(pattern)
        await session.commit()

    # Вызываем функцию save_cheque_from_json
    async with AsyncSession() as session:
        result = await save_cheque_from_json(
            session=session,
            json_data=json_data,
            file_name="test_file.json",
            user="test_user",
        )
        await session.commit()

    if expected_result is not None:
        assert result == "Cheque added to database"
    else:
        # В случае, если паттерн не применился, чек всё равно добавится
        assert result == "Cheque added to database"

    # Проверяем, что чек добавлен
    stmt = select(Cheque).where(Cheque.file_name == "test_file.json")
    async with AsyncSession() as session:
        result_cheque = await session.execute(stmt)
        cheque = result_cheque.scalars().first()
    assert cheque is not None
    assert cheque.user == "test_user"
    assert cheque.seller == json_data["data"]["json"]["user"]
    assert cheque.total == json_data["data"]["json"]["totalSum"] / 100

    # Проверяем детали чека
    async with AsyncSession() as session:
        stmt_detail = select(ChequeDetail).where(ChequeDetail.cheque_id == cheque.id)
        details = (await session.execute(stmt_detail)).scalars().all()
    assert len(details) == len(json_data["data"]["json"]["items"])
    for detail in details:
        if expected_result:
            assert detail.category == expected_result
        else:
            assert not detail.category
