from typing import Optional
from http import HTTPStatus

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.crud.base import CRUDBase
from app.models import Goal, Ipr, Status, User, Competency, CompetencyIpr


class IPRCrud(CRUDBase):
    async def check_ipr_exists(self,
                               ipr_id: int,
                               session: AsyncSession) -> Ipr:
        ipr = await self.get_ipr_by_id(ipr_id, session)
        if ipr is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="ИПР не найден."
            )
        return ipr

    async def get_status_id_by_name(self,
                                    status_name: str,
                                    session: AsyncSession) -> Optional[int]:

        status_id = await session.execute(
            select(Status.id).where(Status.name == status_name)
        )
        status_id = status_id.scalars().first()
        return status_id

    async def get_status_by_id(self,
                               status_id: int,
                               session: AsyncSession) -> Optional[str]:

        status_name = await session.execute(
            select(Status.name).where(Status.id == status_id)
        )
        status_name = status_name.scalars().first()
        return status_name

    async def get_ipr_by_id(self,
                            ipr_id: int,
                            session: AsyncSession) -> Optional[Ipr]:
        ipr = await session.execute(select(Ipr).where(Ipr.id == ipr_id))
        ipr = ipr.scalars().first()
        if ipr is None:
            raise HTTPException(
                HTTPStatus.NOT_FOUND, detail=f"IPR с id - {ipr_id} не существует"
            )

        return ipr

    async def check_ipr_user(self,
                             ipr,
                             user: User) -> None:
        if ipr.employee_id != user.id or ipr.supervisor_id != user.id:
            raise HTTPException(
                HTTPStatus.FORBIDDEN,
                detail="У вас нет прав модифицировать/удалять данный ИПР",
            )

    async def get_goal_id_by_name(self,
                                  goal,
                                  session) -> int:
        query = select(Goal.id).where(Goal.name == goal)
        goal_id = await session.execute(query)
        goal_id = goal_id.scalars().first()
        return goal_id

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


ipr_crud = IPRCrud(Ipr)
goal_crud = CRUDBase(Goal)
competency_crud = CRUDBase(Competency)
competency_ipr_crud = CRUDBase(CompetencyIpr)
