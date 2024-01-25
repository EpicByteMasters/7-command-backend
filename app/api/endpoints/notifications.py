# from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user
# from app.crud.notifications import check_notifications, get_user_notifications
from app.models import User
from app.schemas.notifications import NotificationGet

router = APIRouter()


@router.get("/notifications",
            response_model=List[NotificationGet],
            dependencies=[Depends(current_user)])
async def get_notifications(user: User = Depends(current_user),
                            session: AsyncSession = Depends(get_async_session)):
    pass
#     await check_notifications(user, session)
#     notifications = await get_user_notifications(user, session)
#     return notifications
