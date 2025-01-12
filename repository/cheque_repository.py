from datetime import datetime

from db.connector import AsyncSession
from db.models import Cheque, ChequeDetail
from sqlalchemy.future import select


async def get_purchase_date_time_from_json_data(json_data: dict):
    """
    Извлекает и преобразовывает дату и время (dateTime)
    (json сервиса ФНС, объект data.json) чека

    :param json_data: часть json-файла (только объект data.json), полученного из сервиса по проверке чеков
    :return: Дата и время чека
    """
    # Извлечение даты и времени покупки из JSON
    purchase_date_str = json_data.get("dateTime")
    if not purchase_date_str:
        raise ValueError("Дата и время покупки отсутствуют в переданном JSON.")
    purchase_date = datetime.fromisoformat(purchase_date_str)  # Конвертация строки в datetime
    return purchase_date


async def save_cheque_from_json(
    session: AsyncSession,
    json_data: dict,
    file_name: str,
    user: str
) -> str:
    # Проверяем, содержит ли json_data необходимые данные
    data = json_data.get('data', {}).get('json', {})

    if not data:
        raise ValueError("Отсутствуют данные чека в переданном JSON.")

    if await exists_cheque(session, data):
        return 'Cheque already exists'

    # Извлечение даты и времени покупки из JSON
    purchase_date = await get_purchase_date_time_from_json_data(data)

    # Создаем объект Cheque
    cheque = Cheque(
        file_name=file_name,
        purchase_date=purchase_date,
        user=user,
        seller=data.get('user'),
        account=data.get('account'),
        notes=data.get('retailPlace'),
        total=float(data.get('totalSum')) / 100,
        created_at=datetime.now(),  # В момент создания
        updated_at=datetime.now()  # В момент создания
    )

    # Добавляем чек в сессию
    session.add(cheque)
    await session.flush()  # Сохраняем чек, чтобы получить его ID для деталей

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

    await session.flush()
    return 'Cheque added to database'


async def exists_cheque(
        session: AsyncSession,
        data: dict,
) -> bool:
    """
    Проверяет наличие записи в таблице
    :param session:
    :param data: часть json-файла (только объект data.json), полученного из сервиса по проверке чеков
    :return: True если такая запись есть, False - если нет
    """

    # Извлекаем дату покупки и другие необходимые поля
    purchase_date = await get_purchase_date_time_from_json_data(data)
    seller = data.get('user')
    total = float(data.get('totalSum')) / 100  # Конвертация в нужный формат

    # Выполняем запрос к базе данных для проверки существования
    query = select(Cheque).filter_by(
        purchase_date = purchase_date,
        seller = seller,
        total = total
    )

    result = await session.execute(query)
    cheque_exists = result.scalars().first() is not None

    return cheque_exists
