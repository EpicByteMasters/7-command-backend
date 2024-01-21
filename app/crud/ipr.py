from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder


from app.core.db import AsyncSessionLocal
from app.models.ipr import Ipr
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
