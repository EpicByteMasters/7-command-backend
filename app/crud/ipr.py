from typing import Optional
from http import HTTPStatus

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import load_only
from fastapi import HTTPException

from app.crud.base import CRUDBase
from app.models import Goal, Ipr, Status, User, Competency, CompetencyIpr, Task


class IPRCrud(CRUDBase):
    async def get_user_iprs(self, user: User, session: AsyncSession):
        query = select(self.model).where(
            self.model.is_deleted == False, self.model.employee_id == user.id  # noqa
        )
        all_objects = await session.execute(query)
        return all_objects.scalars().all()

    async def get_user_ipr(self, ipr_id, session: AsyncSession):
        query = select(Ipr).where(
            Ipr.id == ipr_id
        ).options(
            load_only(
                Ipr.goal,
                Ipr.specialty,
                Ipr.create_date,
                Ipr.close_date,
                Ipr.mentor_id,
                Ipr.description,
                Ipr.comment,
                Ipr.ipr_status
            )
        )

        ipr_result = await session.execute(query)
        ipr_obj = ipr_result.scalar_one_or_none()
        task_query = select(Task).where(Task.ipr_id == ipr_id)
        tasks_result = await session.execute(task_query)
        tasks = tasks_result.scalars().all()
        ipr_obj.tasks = tasks
        return ipr_obj

    async def check_ipr_exists(self, ipr_id: int, session: AsyncSession) -> Ipr:
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

    async def check_ipr_user(self, ipr, user: User) -> None:
        if ipr.employee_id != user.id or ipr.supervisor_id != user.id:
            raise HTTPException(
                HTTPStatus.FORBIDDEN,
                detail="У вас нет прав модифицировать/удалять данный ИПР",
            )

    async def check_user_is_ipr_emloyee(self,
                                        ipr_id: int,
                                        user: User,
                                        session: AsyncSession):
        ipr = await self.get_ipr_by_id(ipr_id, session)
        if ipr.employee_id != user.id:
            raise HTTPException(
                HTTPStatus.FORBIDDEN,
                detail="У вас нет прав просматривать данный ИПР",
            )

    async def get_goal_id_by_name(self, goal, session) -> int:
        query = select(Goal.id).where(Goal.name == goal)
        goal_id = await session.execute(query)
        goal_id = goal_id.scalars().first()
        return goal_id


ipr_crud = IPRCrud(Ipr)
goal_crud = CRUDBase(Goal)
competency_crud = CRUDBase(Competency)
competency_ipr_crud = CRUDBase(CompetencyIpr)
