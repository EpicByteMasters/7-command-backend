from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.schemas.ipr import IprListRead
from app.core.user import current_user
from app.models.user import User

router = APIRouter()


@router.get(
    "/",  # {take}{skip}{statusipr}
    response_model=list[IprListRead],
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)]
)
async def get_iprs(take: int,
                   skip: int,
                   statusipr: str = None,
                   user: User = Depends(current_user),
                   session: AsyncSession = Depends(get_async_session),
                   ):

    pass
