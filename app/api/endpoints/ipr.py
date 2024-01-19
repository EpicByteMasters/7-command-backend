from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from app.core.db import get_async_session
from app.schemas.ipr import IPRDraftSave

router = APIRouter()


@router.put('/mentor/iprs/ipr/:id/save-draft',
            response_model=IPRDraftSave
            )
async def save_draft(
        session: AsyncSession = Depends(get_async_session),
        # user: User = Depends(get_current_user())
):
    pass
