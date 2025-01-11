from sqlalchemy.future import select
from sqlalchemy import and_, or_
from typing import List

from db.connector import AsyncSession
from db.models import ChequeDetail, Cheque
from repository.get_cheques_repository import get_comparison_operation
from schemas.cheque_schemas import ChequeDetailsFilterSchema


async def get_cheque_details(
    session: AsyncSession,
    filters: ChequeDetailsFilterSchema
) -> List[ChequeDetail]:
    query = select(ChequeDetail).join(Cheque)

    conditions = []

    if filters.start_date:
        conditions.append(Cheque.purchase_date >= filters.start_date)
    if filters.end_date:
        conditions.append(Cheque.purchase_date <= filters.end_date)
    if filters.seller:
        conditions.append(Cheque.seller == filters.seller)
    if filters.notes:
        conditions.append(Cheque.notes.ilike(f'%{filters.notes}%'))
    if filters.item_name:
        conditions.append(ChequeDetail.name.ilike(f'%{filters.item_name}%'))

    total_condition = get_comparison_operation(Cheque.total, filters.total_op, filters.total_value)
    if total_condition is not None:
        conditions.append(total_condition)

    item_price_condition = get_comparison_operation(ChequeDetail.price, filters.item_price_op, filters.item_price_value)
    if item_price_condition is not None:
        conditions.append(item_price_condition)

    item_total_condition = get_comparison_operation(ChequeDetail.total, filters.item_total_op, filters.item_total_value)
    if item_total_condition is not None:
        conditions.append(item_total_condition)

    # Общий поиск по строковым полям
    if filters.search:
        search_pattern = f'%{filters.search}%'
        search_conditions = or_(
            Cheque.file_name.ilike(search_pattern),
            Cheque.user.ilike(search_pattern),
            Cheque.seller.ilike(search_pattern),
            Cheque.account.ilike(search_pattern),
            Cheque.notes.ilike(search_pattern),
            ChequeDetail.name.ilike(search_pattern),
            ChequeDetail.category.ilike(search_pattern)
        )
        conditions.append(search_conditions)

    if conditions:
        query = query.where(and_(*conditions))

    # Добавляем сортировку
    query = query.order_by(Cheque.purchase_date)

    result = await session.execute(query)
    cheque_details = result.scalars().all()

    return cheque_details
