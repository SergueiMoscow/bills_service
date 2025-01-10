from datetime import datetime
from typing import Optional, List

from sqlalchemy import select, and_

from db.connector import AsyncSession
from db.models import Cheque
from schemas.cheque_schemas import ChequeFilter


async def get_cheques(session: AsyncSession, filters: ChequeFilter) -> List[Cheque]:
    """
    Получение чеков с учетом фильтров.

    :param session: Открытая сессия AsyncSession
    :param filters: Объект ChequeFilter с фильтрами
    :return: Список объектов Cheque
    """
    query = select(Cheque)
    filter_conditions = []

    if filters.start_date:
        filter_conditions.append(Cheque.purchase_date >= filters.start_date)
    if filters.end_date:
        filter_conditions.append(Cheque.purchase_date <= filters.end_date)
    if filters.seller:
        filter_conditions.append(Cheque.seller.ilike(f"%{filters.seller}%"))
    if filters.category:
        filter_conditions.append(Cheque.category.ilike(f"%{filters.category}%"))
    if filters.notes:
        filter_conditions.append(Cheque.notes.ilike(f"%{filters.notes}%"))
    if filters.total_op and filters.total_value is not None:
        total_operations = {
            '<': Cheque.total < filters.total_value,
            '<=': Cheque.total <= filters.total_value,
            '=': Cheque.total == filters.total_value,
            '>': Cheque.total > filters.total_value,
            '>=': Cheque.total >= filters.total_value
        }
        operation = total_operations.get(filters.total_op)
        if operation is not None:
            filter_conditions.append(operation)

    if filter_conditions:
        query = query.where(and_(*filter_conditions))

    # Добавляем сортировку по purchase_date в порядке возрастания
    query = query.order_by(Cheque.purchase_date.asc())

    result = await session.execute(query)
    return result.scalars().all()
