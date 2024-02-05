import datetime

from sqlalchemy import select, and_, not_
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import CRUDBase
from app.models import User, Notification, Ipr, Task
from app.schemas.notifications import NotificationGet


class NotificationCRUD(CRUDBase):
    async def check_ipr_closed(self, user: User, session: AsyncSession):
        query_ipr = select(Ipr).where(
            and_(
                Ipr.close_date <= datetime.date.today(),
                Ipr.ipr_status_id == "IN_PROGRESS",
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
                brief_text="Истек срок плана развития. Руководителю необходимо подвести итоги и оценить достижение цели",
                date=ipr_closed_obj.close_date,
                url=f"http://link/{ipr_closed_obj.ipr_id}",
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
        for task_closed_obj in task_closed_objs:
            msg = NotificationGet(
                title="Истек срок задачи",
                briefText="Истек срок задачи.",
                date=task_closed_obj.close_date
            ).dict()

            msg.pop("url")
            msg["user_id"] = user.id
            msg["task_id"] = task_closed_obj.id
            msg["url"] = f"http://link/{task_closed_obj.ipr_id}"
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
        link_id = (
            (await session.execute(
                select(Ipr.id).where(Ipr.employee_id == user.id)
            ))
            .unique()
            .scalars()
            .first()
        )
        return [
            NotificationGet(
                title=notification.title,
                brief_text=notification.brief_text,
                date=notification.date,
                url=f"http://link/{link_id}",
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
