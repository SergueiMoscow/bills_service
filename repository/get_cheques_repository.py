from datetime import datetime
from typing import Optional, List

from sqlalchemy import select, and_

from db.connector import AsyncSession
from db.models import Cheque


async def get_cheques(
    session: AsyncSession,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    seller: Optional[str] = None,
    notes: Optional[str] = None,
    total_op: Optional[str] = None,
    total_value: Optional[float] = None
) -> List[Cheque]:
    """
    Получение чеков с учетом фильтров.

    :param session: Открытая сессия AsyncSession
    :param start_date: Начальная дата для фильтрации по покупке
    :param end_date: Конечная дата для фильтрации по покупке
    :param seller: Продавец для фильтрации
    :param notes: Заметки для фильтрации
    :param total_op: Операция для фильтрации по общей сумме
    :param total_value: Значение для фильтрации по общей сумме
    :return: Список объектов Cheque
    """

    query = select(Cheque)  # Начинаем с выборки чеков

    filters = []

    if start_date:
        filters.append(Cheque.purchase_date >= start_date)
    if end_date:
        filters.append(Cheque.purchase_date <= end_date)
    if seller:
        filters.append(Cheque.seller == seller)
    if notes:
        filters.append(Cheque.notes.ilike(f'%{notes}%'))  # Нечувствительный к регистру поиск
    if total_op and total_value is not None:
        total_operations = {
            '<': Cheque.total < total_value,
            '<=': Cheque.total <= total_value,
            '=': Cheque.total == total_value,
            '>': Cheque.total > total_value,
            '>=': Cheque.total >= total_value
        }
        filters.append(total_operations.get(total_op))

    if filters:
        query = query.where(and_(*filters))

    result = await session.execute(query)
    cheques = result.scalars().all()

    return cheques