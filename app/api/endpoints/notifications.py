from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user
from app.crud import notification_crud
from app.models import User
from app.schemas.notifications import NotificationGet

router = APIRouter()


@router.get("/notifications",
            response_model=list[NotificationGet],
            dependencies=[Depends(current_user)],
            summary="Запрос на последние уведомления")
async def get_notifications(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    notifications = await notification_crud.get_user_notifications(user,
                                                                   session)
    return notifications
