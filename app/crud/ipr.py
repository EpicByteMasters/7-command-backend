from typing import Optional
from http import HTTPStatus

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, delete, desc, select
from fastapi import HTTPException

from app.crud.base import CRUDBase
from app.models import (
    Competency,
    CompetencyIpr,
    EducationTask,
    Goal,
    Ipr,
    Status,
    Task,
    User
)


class IPRCrud(CRUDBase):

    async def create_ipr_draft(self, obj_in, user_id: int, session: AsyncSession):
        obj_in_data = obj_in.dict()
        obj_in_data["ipr_status_id"] = "DRAFT"
        obj_in_data["supervisor_id"] = user_id
        db_obj = Ipr(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_users_ipr(self, user: User, session: AsyncSession):
        query = select(Ipr).where(
            Ipr.is_deleted == False,  # noqa
            Ipr.employee_id == user.id,
            Ipr.ipr_status_id != "DRAFT"
        )
        all_objects = await session.execute(query)
        return all_objects.unique().scalars().all()

    async def check_ipr_exists(self,
                               ipr_id: int,
                               session: AsyncSession) -> Ipr:
        ipr = await self.get_ipr_by_id(ipr_id, session)
        if ipr is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="ИПР не найден."
            )
        return ipr

    async def get_status_id_by_name(
        self, status_name: str, session: AsyncSession
    ) -> Optional[int]:

        status_id = await session.execute(
            select(Status.id).where(Status.name == status_name)
        )
        status_id = status_id.scalars().first()
        return status_id

    async def get_status_by_id(
        self,
        status_id: int,
        session: AsyncSession,
    ) -> Optional[str]:

        status_name = await session.execute(
            select(Status.name).where(Status.id == status_id)
        )
        status_name = status_name.scalars().first()
        return status_name

    async def get_ipr_by_id(self, ipr_id: int, session: AsyncSession):
        ipr = await session.execute(select(Ipr).where(Ipr.id == ipr_id))
        ipr = ipr.scalars().first()
        if ipr is None:
            raise HTTPException(
                HTTPStatus.NOT_FOUND, detail=f"IPR с id - {ipr_id} не существует"
            )

        return ipr

    async def remove_ipr(self,
                         user: User,
                         ipr_id: int,
                         session: AsyncSession):
        ipr = await self.get_ipr_by_id(ipr_id, session)
        await self.check_ipr_user(ipr, user)
        ipr.is_deleted = True
        session.add(ipr)
        await session.commit()
        return

    async def remove_all_tasks_from_ipr(self, ipr_id, session: AsyncSession):
        ipr_tasks = select(Task.id).where(Task.ipr_id == ipr_id)
        ipr_tasks = await session.execute(ipr_tasks)
        ipr_tasks = ipr_tasks.scalars().all()
        for task_id in ipr_tasks:
            await session.execute(delete(
                EducationTask).where(
                    EducationTask.task_id == task_id))
        query_tasks = delete(Task).where(Task.ipr_id == ipr_id)
        await session.execute(query_tasks)
        return

    async def check_user_does_not_have_active_iprs(self,
                                                   user_id: int,
                                                   session: AsyncSession):
        query = select(Ipr).where(
            and_(Ipr.ipr_status_id == "IN_PROGRESS",
                 Ipr.employee_id == user_id))
        result = await session.execute(query)
        result = result.scalar()
        if result:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail="Этот пользователь уже имеет активный ИПР")
        return

    async def to_work(self, ipr: Ipr, session: AsyncSession):
        ipr.ipr_status_id = "IN_PROGRESS"
        query = select(Task.close_date).where(
            Task.ipr_id == ipr.id).order_by(
                desc(Task.close_date)).limit(1)
        latest_task_date = await session.execute(query)
        latest_task_date = latest_task_date.scalar()
        ipr.close_date = latest_task_date
        session.add(ipr)
        return ipr


class CompetencyIprCrud(CRUDBase):

    async def remove_all_competencies_from_ipr(self, ipr_id, session: AsyncSession):
        query = delete(CompetencyIpr).where(CompetencyIpr.ipr_id == ipr_id)
        await session.execute(query)
        await session.commit()
        return


status_crud = IPRCrud(Status)
ipr_crud = IPRCrud(Ipr)
goal_crud = CRUDBase(Goal)
competency_crud = CRUDBase(Competency)
competency_ipr_crud = CompetencyIprCrud(CompetencyIpr)
