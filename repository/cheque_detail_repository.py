from sqlalchemy.future import select
from sqlalchemy import and_, or_
from datetime import datetime
from typing import List, Optional

from db.connector import AsyncSession
from db.models import ChequeDetail, Cheque
from schemas.cheque_schemas import ChequeDetailsFilter


async def get_cheque_details(
    session: AsyncSession,
    filters: ChequeDetailsFilter
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
    if filters.total_op and filters.total_value is not None:
        total_operations = {
            '<': Cheque.total < filters.total_value,
            '<=': Cheque.total <= filters.total_value,
            '=': Cheque.total == filters.total_value,
            '>': Cheque.total > filters.total_value,
            '>=': Cheque.total >= filters.total_value
        }
        conditions.append(total_operations.get(filters.total_op))
    if filters.item_name:
        conditions.append(ChequeDetail.name.ilike(f'%{filters.item_name}%'))
    if filters.item_price_op and filters.item_price_value is not None:
        price_operations = {
            '<': ChequeDetail.price < filters.item_price_value,
            '<=': ChequeDetail.price <= filters.item_price_value,
            '=': ChequeDetail.price == filters.item_price_value,
            '>': ChequeDetail.price > filters.item_price_value,
            '>=': ChequeDetail.price >= filters.item_price_value
        }
        conditions.append(price_operations.get(filters.item_price_op))
    if filters.item_total_op and filters.item_total_value is not None:
        item_total_operations = {
            '<': ChequeDetail.total < filters.item_total_value,
            '<=': ChequeDetail.total <= filters.item_total_value,
            '=': ChequeDetail.total == filters.item_total_value,
            '>': ChequeDetail.total > filters.item_total_value,
            '>=': ChequeDetail.total >= filters.item_total_value
        }
        conditions.append(item_total_operations.get(filters.item_total_op))

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
