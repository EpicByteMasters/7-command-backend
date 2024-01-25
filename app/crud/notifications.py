# import datetime

# from sqlalchemy.ext.asyncio import AsyncSession

<<<<<<< HEAD
from sqlalchemy import select, and_, not_
from app.models import User, Notification, Ipr, Task
from app.schemas.notifications import NotificationGet


async def check_ipr_closed(user: User,
                           session: AsyncSession
                           ):
    query_ipr = (
        select(Ipr)
        .where(and_(
            Ipr.close_date <= datetime.date.today(),
            not_(Ipr.id.in_(
                select(Notification.ipr_id)
                .where(Notification.user_id == user.id))))))

    ipr_closed_objs = (await session.execute(query_ipr)).scalars().all()
    for ipr_closed_obj in ipr_closed_objs:
        msg = NotificationGet(
            title='Истек срок плана развития',
            briefText='Истек срок плана развития. Руководителю необходимо подвести итоги и оценить достижение цели',
            date=ipr_closed_obj.close_date,
            url=f'http://link/{ipr_closed_obj.id}',
        ).dict()

        msg.pop('url')
        msg['user_id'] = user.id
        msg['ipr_id'] = ipr_closed_obj.id
        obj = Notification(**msg)
        print(1)
        session.add(obj)
        await session.commit()
        await session.refresh(obj)


async def check_task_closed(user: User,
                            session: AsyncSession):
    query_task = (
        select(Task)
        .where(and_(
            Task.close_date <= datetime.date.today(),
            not_(Task.id.in_(
                select([Notification.task_id])
                .where(Notification.user_id == user.id)
            ))
        ))
    )
    task_closed_objs = (await session.execute(query_task)).scalars().all()
    print(2)
    for task_closed_obj in task_closed_objs:
        msg = NotificationGet(
            title='Истек срок задачи',
            briefText='Истек срок задачи.',
            date=task_closed_obj.close_date,
            url=f'http://link/{task_closed_obj.id}',
        ).dict()

        msg.pop('url')
        msg['user_id'] = user.id
        msg['task_id'] = task_closed_obj.id
        obj = Notification(**msg)
        print(2)
        session.add(obj)
        await session.commit()
        await session.refresh(obj)


async def get_user_notifications(user: User,
                                 session: AsyncSession):
    await check_ipr_closed(user, session)
    await check_task_closed(user, session)
    query = select(Notification).where(Notification.user_id == user.id)
    result = (await session.execute(query)).scalars().all()
    link_id = (await session.execute(select(Ipr.id).where(Ipr.employee_id == user.id))).scalars().first()
    return [NotificationGet(
        title=notification.title,
        briefText=notification.briefText,
        date=notification.date,
        url=f'http://link/{link_id}'
    ) for notification in result]
=======
# from sqlalchemy import select, join
# from app.models import User, Notification, Ipr, Task
# from app.schemas.notifications import NotificationGet


# async def check_notifications(user: User,
#                               session: AsyncSession):
#     query_ipr = select(Ipr).where(Ipr.id == user.id and Ipr.close_date <= datetime.date.today())
#     query_task = (select(Task).select_from(join(Task, TaskIpr, Task.id == TaskIpr.task_id)
#                                            ).join(Ipr, TaskIpr.ipr_id == Ipr.id
#                                                   ).join(User, User.id == Ipr.emplyee_id
#                                                          ).where(
#         User.id == user.id and Task.close_date <= datetime.date.today()))
#     ipr_closed_obj = (await session.execute(query_ipr)).scalars().first()
#     if ipr_closed_obj is not None:
#         msg = (NotificationGet(
#             title='Истек срок плана развития',
#             briefText='Истек срок плана развития. Руководителю необходимо подвести итоги и оценить достижение цели',
#             date=ipr_closed_obj.close_date,
#             url=f'http://link/{ipr_closed_obj.id}'
#         )).dict()
#         obj = Notification(**msg)
#         await session.add(obj)
#         session.commit()
#         session.refresh(obj)
#     ipr_closed_obj = (await session.execute(query_task)).scalars().all()
#     if ipr_closed_obj is not None:
#         for task in ipr_closed_obj:
#             msg = (NotificationGet(
#                 title='Истек срок задачи.',
#                 briefText='Истек срок задачи.',
#                 date=task.close_date,
#                 url=f'http://link/{task.id}'
#             )).dict()
#             obj = Notification(**msg)
#             await session.add(obj)
#             session.commit()
#             session.refresh(obj)


# async def get_user_notifications(user: User,
#                                  session: AsyncSession):
#     query = select(Notification).where(Notification.user_id == user.id)
#     result = (await session.execute(query)).scalars().all()
#     link_id = (await session.execute(select(Ipr.id).where(Ipr.emplyee_id == user.id))).scalars().first()
#     return [NotificationGet(
#         title=notification.title,
#         briefText=notification.briefText,
#         date=notification.date,
#         url=f'http://link/{link_id}'
#     ) for notification in result]
>>>>>>> develop
