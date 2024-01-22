from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select

from app.core.db import AsyncSessionLocal
from app.models.ipr import Ipr, Status
from app.schemas.ipr import IPRDraftCreate


async def create_ipr(draft_ipr: IPRDraftCreate, session: AsyncSession) -> Ipr:

    draft_ipr_data = draft_ipr.dict()

    db_draft_ipr = Ipr(**draft_ipr_data)
    session.add(db_draft_ipr)

    await session.commit()
    await session.refresh(db_draft_ipr)
    return db_draft_ipr


async def delete_ipr(db_ipr: Ipr, session: AsyncSession) -> Ipr:
    await session.delete(db_ipr)
    await session.commit()
    return db_ipr


async def check_ipr_exists(
    ipr_id: int,
    session: AsyncSession,
) -> Ipr:
    ipr = await get_ipr_by_id(ipr_id, session)
    if ipr is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="ИПР не найден.")
    return ipr


async def get_status_id_by_name(
    status_name: str,
    session: AsyncSession,
) -> Optional[int]:

    status_id = await session.execute(
        select(Status.id).where(Status.name == status_name)
    )
    status_id = status_id.scalars().first()
    return status_id


async def get_status_by_id(
    status_id: int,
    session: AsyncSession,
) -> Optional[str]:

    status_name = await session.execute(
        select(Status.name).where(Status.id == status_id)
    )
    status_name = status_name.scalars().first()
    return status_name


async def get_ipr_by_id(ipr_id: int, session: AsyncSession) -> Optional[Ipr]:
    ipr = await session.execute(select(Ipr).where(Ipr.id == ipr_id))
    ipr = ipr.scalars().first()
    return ipr
