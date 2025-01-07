import aiohttp

from db.models import ChequeDetail, Cheque
from settings import PROVERKACHEKA_TOKEN, PROVERKACHEKA_URL
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone


async def get_cheque_from_api_service(qrraw: str):
    data = {
        "token": PROVERKACHEKA_TOKEN,
        "qrraw": qrraw,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(PROVERKACHEKA_URL, json=data) as response:
            if response.status == 200:
                return await response.json()
            else:
                error_message = await response.text()
                print(f"Error: {response.status}, Message: {error_message}")
                return None


async def save_cheque_from_json(
    session: AsyncSession,
    json_data: dict,
    file_name: str,
    user: str
):
    # Проверяем, содержит ли json_data необходимые данные
    data = json_data.get('data', {}).get('json', {})

    if not data:
        raise ValueError("Отсутствуют данные чека в переданном JSON.")

    # Извлечение даты и времени покупки из JSON
    purchase_date_str = data.get("dateTime")
    if not purchase_date_str:
        raise ValueError("Дата и время покупки отсутствуют в переданном JSON.")
    purchase_date = datetime.fromisoformat(purchase_date_str)  # Конвертация строки в datetime

    # Создаем объект Cheque
    cheque = Cheque(
        file_name=file_name,
        purchase_date=purchase_date,
        user=user,
        seller=data.get('user'),
        notes=data.get('retailPlace'),
        total=float(data.get('totalSum')) / 100,
        created_at=datetime.now(),  # В момент создания
        updated_at=datetime.now()  # В момент создания
    )

    # Добавляем чек в сессию
    session.add(cheque)
    await session.commit()  # Сохраняем чек, чтобы получить его ID для деталей

    # Получаем ID созданного чека
    cheque_id = cheque.id

    # Сохраняем детали
    for item in data.get('items', []):
        cheque_detail = ChequeDetail(
            cheque_id=cheque_id,
            name=item.get("name"),  # Наименование товара
            price=item.get("price"),  # Цена
            quantity=item.get("quantity", 1.0),  # Количество
            total=item.get("sum"),  # Общая сумма
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        session.add(cheque_detail)

    await session.commit()  # Сохраняем детали чека
