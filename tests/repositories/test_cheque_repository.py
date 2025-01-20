import pytest
from sqlalchemy.orm import selectinload

from db.connector import AsyncSession
from db.models import Cheque
from repository.cheque_repository import exists_cheque, save_cheque_from_json
from sqlalchemy import select

from repository.get_cheques_repository import get_cheque_by_id


@pytest.mark.usefixtures('apply_migrations')
@pytest.mark.asyncio
async def test_exists_cheque(json_fixture):
    async with AsyncSession() as session:
        data = json_fixture['data']['json']
        cheque_exists = await exists_cheque(session, data)
        assert cheque_exists is False


@pytest.mark.usefixtures('apply_migrations')
@pytest.mark.asyncio
async def test_save_cheque_from_json(json_fixture):
    file_name = 'test filename'
    async with AsyncSession() as session:
        await save_cheque_from_json(
            session=session,
            json_data=json_fixture,
            file_name=file_name,
            user='test user',
        )
        await session.commit()

    async with AsyncSession() as session:
        stmt = (select(Cheque)
                .options(selectinload(Cheque.details))
                .where(Cheque.file_name == file_name))
        result = await session.execute(stmt)
        cheque = result.scalars().first()

        assert cheque is not None
        assert cheque.total == json_fixture['data']['json']['totalSum'] / 100
        assert cheque.details[0].price == 599
        assert cheque.details[0].total == 599


@pytest.mark.usefixtures('apply_migrations')
@pytest.mark.asyncio
async def test_save_cheque_from_json_error_duplicated(json_fixture):
    async with AsyncSession() as session:
        await save_cheque_from_json(
            session=session,
            json_data=json_fixture,
            file_name='test filename',
            user='test user',
        )
        await session.commit()

    async with AsyncSession() as session:
        saved_duplicated = await save_cheque_from_json(
            session=session,
            json_data=json_fixture,
            file_name='test filename',
            user='test user',
        )
        await session.commit()

    async with AsyncSession() as session:
        result = await session.execute(select(Cheque))
        cheques = result.scalars().all()

    assert len(cheques) == 1
    assert saved_duplicated == 'Cheque already exists'