from datetime import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Ipr, User
from app.schemas.notifications import NotificationGet

user_websockets = {}


async def check_ipr_dates(user_id: int,
                          session: AsyncSession
                          ):
    async with session.begin():
        today_date = datetime.today().strftime("%Y-%m-%d")
        query = select(Ipr).where(Ipr.user_id == user_id, Ipr.close_date == today_date)
        ipr_records = (await session.execute(query)).scalars().all()

        if ipr_records:
            for ipr_record in ipr_records:
                user = await get_user_by_id(user_id, session)
                if user:
                    notification_data = NotificationGet(
                        id=ipr_record.id,
                        idUrl=f"/myteam/iprs/ipr/{ipr_record.id}",
                        task_id=ipr_record.task_id,
                        message=("Истек срок плана развития."
                                 "Руководителю необходимо подвести итоги и оценить достижение цели"),
                    )
                    await send_notification(user, notification_data)


async def other_notification_triggers(user_id: int,
                                      session: AsyncSession,
                                      notification: NotificationGet
                                      ):

    return await send_notification(get_user_by_id(user_id,
                                                  session
                                                  ),
                                   notification
                                   )


async def send_notification(user: User, notification_data: NotificationGet):
    if user.id in user_websockets:
        websocket = user_websockets[user.id]
        await websocket.send_json(jsonable_encoder(notification_data))


async def get_user_by_id(user_id: int,
                         session: AsyncSession
                         ):
    user = await session.execute(select(User).where(User.id == user_id))
    return user.scalar()
