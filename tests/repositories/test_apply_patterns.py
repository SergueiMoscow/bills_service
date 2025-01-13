import pytest
from datetime import datetime

from db.connector import AsyncSession
from db.models import Pattern, ChequeDetail
from repository.get_cheques_repository import get_cheque_by_id
from repository.apply_patterns import apply_patterns


@pytest.mark.usefixtures('apply_migrations')
@pytest.mark.parametrize(
    "model_type, initial_data, patterns, expected_outcome",
    [
        # Тестирование обновления поля в Cheque
        (
            'Cheque',
            {
                'purchase_date': datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
                'seller': "Special Seller",
                'notes': "This is a special sale",
                'total': 200,
                'commit': True
            },
            [
                Pattern(model_in='Cheque', model_out='Cheque', field_in='notes', include='special', field_out='notes', value_out='Updated Notes')
            ],
            {
                'notes': 'Updated Notes'
            }
        ),
        # Тестирование обновления поля в ChequeDetail
        (
            'Cheque',
            {
                'purchase_date': datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
                'seller': "Regular Seller",
                'notes': "Regular sale",
                'total': 100,
                'commit': True
            },
            [
                Pattern(model_in='Cheque', model_out='ChequeDetail', field_in='seller', include='Regular', field_out='name', value_out='Updated Item')
            ],
            {
                'details': {'name': 'Updated Item'}
            }
        ),
        # Тестирование случая, когда паттерн не совпадает
        (
            'Cheque',
            {
                'purchase_date': datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
                'seller': "Unknown Seller",
                'notes': "Unknown sale",
                'total': 150,
                'commit': True
            },
            [
                Pattern(model_in='Cheque', model_out='Cheque', field_in='notes', include='special', field_out='notes', value_out='Should Not Update')
            ],
            {
                'notes': 'Unknown sale'
            }
        ),
        # Тестирование неизвестной модели_out
        (
            'Cheque',
            {
                'purchase_date': datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
                'seller': "Test Seller",
                'notes': "Test sale",
                'total': 300,
                'commit': True
            },
            [
                Pattern(model_in='Cheque', model_out='UnknownModel', field_in='notes', include='Test', field_out='notes', value_out='Attempt to Update')
            ],
            {
                'notes': 'Test sale'  # Должно остаться без изменений
            }
        ),
        # Тестирование отсутствия поля field_in
        (
            'ChequeDetail',
            {
                'name': 'Item 1',
                'price': 50.0,
                'quantity': 2,
                'cheque_id': 1,
                'commit': True
            },
            [
                Pattern(model_in='ChequeDetail', model_out='ChequeDetail', field_in='nonexistent_field', include='Test', field_out='price', value_out='100.0')
            ],
            {
                'price': 50.0  # Должно остаться без изменений
            }
        ),
    ]
)
@pytest.mark.asyncio
async def test_apply_patterns(model_type, initial_data, patterns, expected_outcome, cheque_creator, cheque_detail_creator):
    # Создаем объект Cheque или ChequeDetail в зависимости от model_type
    if model_type == 'Cheque':
        cheque = cheque_creator(
            purchase_date=initial_data['purchase_date'],
            seller=initial_data['seller'],
            notes=initial_data['notes'],
            total=initial_data['total'],
            commit=initial_data['commit']
        )
        obj = cheque
    elif model_type == 'ChequeDetail':
        cheque = cheque_creator(
            purchase_date=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
            seller="Seller",
            notes="Notes",
            total=100,
            commit=True
        )
        cheque_detail = cheque_detail_creator(
            cheque_id=cheque.id,
            name=initial_data['name'],
            price=initial_data['price'],
            quantity=initial_data['quantity'],
            commit=initial_data['commit']
        )
        obj = cheque_detail
    else:
        pytest.fail(f"Unsupported model_type: {model_type}")

    # Добавляем паттерны в базу данных
    async with AsyncSession() as session:
        for pattern in patterns:
            session.add(pattern)
        await session.commit()

        # Вызываем функцию apply_patterns
    async with AsyncSession() as session:
        await apply_patterns(session, obj)
        await session.commit()

    # Проверяем результаты
    async with AsyncSession() as session:
        if model_type == 'Cheque':
            try:
                updated_cheque = await get_cheque_by_id(session, obj.id)
            except Exception as e:
                print(f"Ошибка при получении чека: {e}")
            for field, expected in expected_outcome.items():
                if field == 'details':
                    # Проверяем связанные ChequeDetail
                    details = updated_cheque.details
                    assert len(details) == len(obj.details)
                    for detail in details:
                        for k, v in expected.items():
                            assert getattr(detail, k) == v, f"Expected {k} to be {v}, got {getattr(detail, k)}"
                else:
                    assert getattr(updated_cheque, field) == expected
        elif model_type == 'ChequeDetail':
            updated_detail = await session.get(ChequeDetail, obj.id)
            for field, expected in expected_outcome.items():
                assert getattr(updated_detail, field) == expected