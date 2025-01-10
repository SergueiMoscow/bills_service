from datetime import datetime
from typing import Optional, List, Any

from sqlalchemy import select, and_, BinaryExpression

from db.connector import AsyncSession
from db.models import Cheque
from schemas.cheque_schemas import ChequeFilter

def get_comparison_operation(
    field: Any,
    op: Optional[str],
    value: Optional[float]
) -> Optional[BinaryExpression]:

    if not op or value is None:
        return None
    operations = {
        '<': field < value,
        '<=': field <= value,
        '=': field == value,
        '>': field > value,
        '>=': field >= value
    }
    return operations.get(op)


async def get_cheques(session: AsyncSession, filters: ChequeFilter) -> List[Cheque]:
    """
    Получение чеков с учетом фильтров.

    :param session: Открытая сессия AsyncSession
    :param filters: Объект ChequeFilter с фильтрами
    :return: Список объектов Cheque
    """
    query = select(Cheque)
    conditions = []

    if filters.start_date:
        conditions.append(Cheque.purchase_date >= filters.start_date)
    if filters.end_date:
        conditions.append(Cheque.purchase_date <= filters.end_date)
    if filters.seller:
        conditions.append(Cheque.seller.ilike(f"%{filters.seller}%"))
    if filters.category:
        conditions.append(Cheque.category.ilike(f"%{filters.category}%"))
    if filters.notes:
        conditions.append(Cheque.notes.ilike(f"%{filters.notes}%"))

    total_condition = get_comparison_operation(Cheque.total, filters.total_op, filters.total_value)
    if total_condition is not None:
        conditions.append(total_condition)

    if conditions:
        query = query.where(and_(*conditions))

    # Добавляем сортировку по purchase_date в порядке возрастания
    query = query.order_by(Cheque.purchase_date.asc())

    result = await session.execute(query)
    return result.scalars().all()
