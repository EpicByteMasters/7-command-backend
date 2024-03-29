import datetime

from sqlalchemy import and_, not_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Ipr, Notification, Task, User
from app.schemas.notifications import NotificationGet


class NotificationCRUD(CRUDBase):
    async def check_ipr_closed(self, user: User, session: AsyncSession):
        query_ipr = select(Ipr).where(
            and_(
                Ipr.close_date <= datetime.date.today(),
                Ipr.ipr_status_id == "IN_PROGRESS",
                Ipr.employee_id == user.id,
                not_(
                    Ipr.id.in_(
                        select(Notification.ipr_id)
                        .where(Notification.user_id == user.id)
                    )
                ),
            )
        )

        ipr_closed_objs = (
            await session.execute(query_ipr)
        ).unique().scalars().all()
        for ipr_closed_obj in ipr_closed_objs:
            msg = NotificationGet(
                title="Истек срок плана развития",
                brief_text="Руководителю необходимо подвести итоги",
                date=ipr_closed_obj.close_date,
                button_text="Перейти к плану",
                url=f"/api/v1/mentor/iprs/ipr/{ipr_closed_obj.id}/employee",
            ).dict()

            msg.pop("url")
            msg["user_id"] = user.id
            msg["ipr_id"] = ipr_closed_obj.id
            obj = Notification(**msg)
            session.add(obj)
            await session.commit()
            await session.refresh(obj)

    async def check_task_closed(self, user: User, session: AsyncSession):
        query_task = select(Task).join(Ipr, Ipr.id == Task.ipr_id).where(
            and_(
                Task.close_date <= datetime.date.today(),
                not_(
                    Task.id.in_(
                        select([Notification.task_id]).where(
                            Notification.user_id == user.id
                        )
                    )
                ),
            )
        )
        task_closed_objs = (
            await session.execute(query_task)
        ).unique().scalars().all()
        for task in task_closed_objs:
            msg = NotificationGet(
                title="Истек срок задачи",
                briefText="Истек срок задачи.",
                button_text="Перейти к задаче",
                date=task.close_date
            ).dict()

            msg.pop("url")
            msg["user_id"] = user.id
            msg["task_id"] = task.id
            msg["url"] = f"/api/v1/mentor/iprs/ipr/{task.ipr_id}/employee"
            obj = Notification(**msg)
            session.add(obj)
            await session.commit()
            await session.refresh(obj)

    async def get_user_notifications(self, user: User, session: AsyncSession):
        await self.check_ipr_closed(user, session)
        await self.check_task_closed(user, session)
        query = (
            select(Notification)
            .where(Notification.user_id == user.id)
            .limit(3)
        )
        result = (await session.execute(query)).unique().scalars().all()

        return [
            NotificationGet(
                title=notification.title,
                brief_text=notification.brief_text,
                date=notification.date,
                url=notification.url,
            )
            for notification in result
        ]

    async def create_notification(self,
                                  notification: Notification,
                                  session: AsyncSession):
        try:
            session.add(notification)
            await session.commit()
            await session.refresh(notification)
        except Exception as e:
            session.rollback()
            raise e
        return notification


notification_crud = NotificationCRUD(Notification)
