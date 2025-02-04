from datetime import datetime
from typing import Optional, List, Any

from sqlalchemy import select, and_, BinaryExpression, or_
from sqlalchemy.orm import selectinload

from db.connector import AsyncSession
from db.models import Cheque
from schemas.cheque_schemas import ChequeFilterSchema

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


async def get_cheques(session: AsyncSession, filters: ChequeFilterSchema) -> List[Cheque]:
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
    if filters.notes:
        conditions.append(Cheque.notes.ilike(f"%{filters.notes}%"))

    total_condition = get_comparison_operation(Cheque.total, filters.total_op, filters.total_value)
    if total_condition is not None:
        conditions.append(total_condition)
    if filters.search:
        search_pattern = f'%{filters.search}%'
        search_conditions = or_(
            Cheque.file_name.ilike(search_pattern),
            Cheque.user.ilike(search_pattern),
            Cheque.seller.ilike(search_pattern),
            Cheque.account.ilike(search_pattern),
            Cheque.notes.ilike(search_pattern),
        )
        conditions.append(search_conditions)

    if conditions:
        query = query.where(and_(*conditions))

    # Добавляем сортировку по purchase_date в порядке возрастания
    query = query.order_by(Cheque.purchase_date.asc())

    result = await session.execute(query)
    return result.scalars().all()


async def get_cheque_by_id(session: AsyncSession, cheque_id: int) -> Optional[Cheque]:
    stmt = (select(Cheque)
            .options(selectinload(Cheque.details))
            .where(Cheque.id == cheque_id))
    result = await session.execute(stmt)
    cheque = result.scalars().first()
    return cheque
