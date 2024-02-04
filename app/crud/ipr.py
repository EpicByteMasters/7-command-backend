from datetime import date
from http import HTTPStatus
from typing import Optional

from sqlalchemy import and_, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.crud.base import CRUDBase
from app.schemas.ipr import IprComplete
from app.models import (
    Competency,
    CompetencyIpr,
    Goal,
    Ipr,
    Status,
    Task,
    User,
)
from app.schemas.ipr import CompetencyIprCreate


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
            Ipr.ipr_status_id != "DRAFT",
        ).order_by(desc(Ipr.create_date))
        all_objects = await session.execute(query)
        return all_objects.unique().scalars().all()

    async def get_users_ipr_by_supervisor(self,
                                          user: User,
                                          session: AsyncSession):
        query = select(Ipr).where(
            Ipr.is_deleted == False,  # noqa
            Ipr.employee_id == user.id
        )
        all_objects = await session.execute(query)
        return all_objects.unique().scalars().all()

    async def get_last_users_ipr(self, user: User, session: AsyncSession):
        query_draft = (
            select(Ipr).where(
                Ipr.is_deleted == False,  # noqa
                Ipr.employee_id == user.id,
                Ipr.ipr_status_id == "DRAFT"
            )
        )
        query_if_no_draft = (
            select(Ipr)
            .where(
                Ipr.is_deleted == False,  # noqa
                Ipr.employee_id == user.id
            )
            .order_by(desc(Ipr.create_date))
            .limit(1)
        )

        draft = await session.execute(query_draft)
        draft = draft.scalar()
        if draft:
            return draft
        all_objects = await session.execute(query_if_no_draft)
        if not all_objects:
            return None
        return all_objects.scalar()

    async def check_ipr_exists(self, ipr_id: int, session: AsyncSession) -> Ipr:
        ipr = await self.get_ipr_by_id(ipr_id, session)
        if ipr is None or ipr.is_deleted is True:
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

        return ipr

    async def remove_ipr(self,
                         ipr_id: int,
                         session: AsyncSession):
        ipr = await self.get_ipr_by_id(ipr_id, session)
        ipr.is_deleted = True
        session.add(ipr)
        await session.commit()
        return

    async def check_user_does_not_have_active_iprs(self,
                                                   user_id: int,
                                                   session: AsyncSession):
        query = select(Ipr).where(
            and_(Ipr.ipr_status_id == "IN_PROGRESS", Ipr.employee_id == user_id)
        )
        result = await session.execute(query)
        result = result.scalar()
        if result:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Этот пользователь уже имеет активный ИПР",
            )
        return

    async def get_mentors_iprs(
        self, take: int, skip: int, statusipr, user: User, session: AsyncSession
    ):
        if take == -1:
            take = None
        if statusipr:
            query = (
                select(self.model)
                .where(
                    self.model.is_deleted == False,  # noqa
                    self.model.mentor_id == user.id,
                    self.model.ipr_status == statusipr,
                )
                .offset(skip)
                .limit(take)
            )
        else:
            query = (
                select(self.model)
                .where(
                    self.model.is_deleted == False,  # noqa
                    self.model.mentor_id == user.id,
                )
                .offset(skip)
                .limit(take)
            )

        all_objects = await session.execute(query)
        return all_objects.unique().scalars().all()

    async def check_user_does_not_have_draft_iprs(self,
                                                  user_id: int,
                                                  session: AsyncSession):
        query = select(Ipr).where(
            and_(Ipr.ipr_status_id == "DRAFT",
                 Ipr.is_deleted == False,  # noqa
                 Ipr.employee_id == user_id))
        result = await session.execute(query)
        result = result.scalar()
        if result:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Для этого пользователя уже создан черновик ИПР"
            )
        return

    async def to_work(self, ipr: Ipr, session: AsyncSession):
        ipr.ipr_status_id = "IN_PROGRESS"
        query = (
            select(Task.close_date)
            .where(Task.ipr_id == ipr.id)
            .order_by(desc(Task.close_date))
            .limit(1)
        )
        latest_task_date = await session.execute(query)
        latest_task_date = latest_task_date.scalar()
        ipr.close_date = latest_task_date
        session.add(ipr)
        return ipr

    async def to_complete(self,
                          ipr: Ipr,
                          ipr_data: IprComplete,
                          session: AsyncSession):
        ipr.ipr_status_id = ipr_data.ipr_status_id
        ipr.ipr_grade = ipr_data.ipr_grade
        ipr.comment = ipr_data.comment

        for task in ipr.task:
            if task.task_status_id in ["IN_PROGRESS", "AWAITING_REVIEW"]:
                task.close_date = date.today()
                task.task_status_id = ipr_data.ipr_status_id
                session.add(task)
        session.add(ipr)
        await session.commit()
        await session.refresh(ipr)
        return ipr

    async def to_cancel(self, ipr: Ipr, session: AsyncSession):
        ipr.ipr_status_id = "CANCELED"

        for task in ipr.task:
            if task.task_status_id in ["IN_PROGRESS", "AWAITING_REVIEW"]:
                task.close_date = date.today()
                task.task_status_id = "CANCELED"
                session.add(task)
        session.add(ipr)
        await session.commit()
        await session.refresh(ipr)
        return ipr

    async def update_ipr(self, obj_in, db_obj, session: AsyncSession):
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True, exclude_none=True)
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj


class CompetencyIprCrud(CRUDBase):

    async def update_competencies(self,
                                  ipr_id,
                                  data_in,
                                  session: AsyncSession):
        query_out = (
            select(CompetencyIpr)
            .where(CompetencyIpr.competency.not_in(data_in),
                   CompetencyIpr.ipr_id == ipr_id)
        )
        query_in = (
            select(Competency.id)
            .join(CompetencyIpr, CompetencyIpr.competency == Competency.id)
            .where(CompetencyIpr.ipr_id == ipr_id)
        )
        result_out = await session.execute(query_out)
        result_in = await session.execute(query_in)
        result_out = result_out.scalars().all()
        result_in = result_in.scalars().all()

        to_delete = []
        for obj in result_out:
            to_delete.append(obj)

        for competency_id in data_in:
            if competency_id not in result_in:
                competency = await competency_crud.get(competency_id, session)
                if competency is None:
                    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                        detail="Такой курс не найден")
                create_dict = {
                    "competency": competency_id,
                    "ipr_id": ipr_id
                }
                data_in = CompetencyIprCreate.parse_obj(create_dict)
                await competency_ipr_crud.create(data_in, session)

        for obj in to_delete:
            await session.delete(obj)


status_crud = IPRCrud(Status)
ipr_crud = IPRCrud(Ipr)
goal_crud = CRUDBase(Goal)
competency_crud = CRUDBase(Competency)
competency_ipr_crud = CompetencyIprCrud(CompetencyIpr)
