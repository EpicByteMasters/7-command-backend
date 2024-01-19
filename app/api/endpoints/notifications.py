from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from fastapi.routing import APIRouter

from app.core.db import get_async_session
from app.schemas.notifications import NotificationGet

router = APIRouter()


@router.get('/notifications',
            response_model=NotificationGet
            # dependencies=[Depends(current_user)]
            )
async def get_notification(session: AsyncSession = Depends(get_async_session),
                           # user: User = Depends(get_current_user())
                           ) -> NotificationGet:
    pass
