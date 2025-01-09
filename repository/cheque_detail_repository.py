from sqlalchemy.future import select
from sqlalchemy import and_
from sqlalchemy.orm import selectinload
from datetime import datetime, timezone
from typing import List, Optional, Tuple, Union

from db.connector import AsyncSession
from db.models import ChequeDetail, Cheque


async def get_cheque_details(
    session: AsyncSession,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    seller: Optional[str] = None,
    notes: Optional[str] = None,
    total_op: Optional[str] = None,
    total_value: Optional[float] = None,
    item_name: Optional[str] = None,
    item_price_op: Optional[str] = None,
    item_price_value: Optional[float] = None,
    item_total_op: Optional[str] = None,
    item_total_value: Optional[float] = None,
) -> List[ChequeDetail]:
    """
    Получение деталей чеков с учетом фильтров.

    :param session: Открытая сессия AsyncSession
    :param start_date: Начальная дата для фильтрации по покупке
    :param end_date: Конечная дата для фильтрации по покупке
    :param seller: Продавец для фильтрации
    :param notes: Заметки для фильтрации
    :param total_op: Операция для фильтрации по общей сумме
    :param total_value: Значение для фильтрации по общей сумме
    :param item_name: Наименование товара для фильтрации
    :param item_price_op: Операция для фильтрации по цене товара
    :param item_price_value: Значение для фильтрации по цене товара
    :param item_total_op: Операция для фильтрации по общей сумме товара
    :param item_total_value: Значение для фильтрации по общей сумме товара
    :return: Список объектов ChequeDetail
    """

    # Начинаем выборку деталей чеков
    query = select(ChequeDetail).join(Cheque)

    filters = []

    if start_date:
        filters.append(Cheque.purchase_date >= start_date)
    if end_date:
        filters.append(Cheque.purchase_date <= end_date)
    if seller:
        filters.append(Cheque.seller == seller)
    if notes:
        filters.append(Cheque.notes.ilike(f'%{notes}%'))  # Используем ilike для нечувствительного к регистру поиска
    if total_op and total_value is not None:
        total_operations = {
            '<': Cheque.total < total_value,
            '<=': Cheque.total <= total_value,
            '=': Cheque.total == total_value,
            '>': Cheque.total > total_value,
            '>=': Cheque.total >= total_value
        }
        filters.append(total_operations.get(total_op))
    if item_name:
        filters.append(ChequeDetail.name.ilike(f'%{item_name}%'))  # Нечувствительный к регистру поиск
    if item_price_op and item_price_value is not None:
        price_operations = {
            '<': ChequeDetail.price < item_price_value,
            '<=': ChequeDetail.price <= item_price_value,
            '=': ChequeDetail.price == item_price_value,
            '>': ChequeDetail.price > item_price_value,
            '>=': ChequeDetail.price >= item_price_value
        }
        filters.append(price_operations.get(item_price_op))
    if item_total_op and item_total_value is not None:
        item_total_operations = {
            '<': ChequeDetail.total < item_total_value,
            '<=': ChequeDetail.total <= item_total_value,
            '=': ChequeDetail.total == item_total_value,
            '>': ChequeDetail.total > item_total_value,
            '>=': ChequeDetail.total >= item_total_value
        }
        filters.append(item_total_operations.get(item_total_op))

    if filters:
        query = query.where(and_(*filters))

    result = await session.execute(query)
    cheque_details = result.scalars().all()

    # Возвращаем только объекты ChequeDetail
    return cheque_details