import datetime
from typing import Optional
from http import HTTPStatus

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from app.crud.base import CRUDBase
from app.models import Ipr, Status, User
from app.schemas.ipr import IPRDraftCreate, IPRDraftReturn


class IPRCrud(CRUDBase):
    async def create_ipr_draft(self,
                               draft_ipr: IPRDraftCreate,
                               session: AsyncSession) -> Ipr:
        draft_ipr_data = draft_ipr.dict()
        db_draft_ipr = Ipr(**draft_ipr_data)
        session.add(db_draft_ipr)
        await session.commit()
        await session.refresh(db_draft_ipr)

        return IPRDraftReturn(id=db_draft_ipr.id, status='DRAFT')

    async def update_ipr_draft(self,
                               ipr_id: int,
                               ipr_draft: IPRDraftCreate,
                               session: AsyncSession) -> HTTPStatus:
        try:
            ipr_obj = await self.get_ipr_by_id(ipr_id)
        except HTTPException as exception:
            return {
                "timestamp": datetime.now().isoformat(),
                "status": exception.status_code,
                "error": "Not Found",
                "errorMessage": exception.detail
            }
        ipr = jsonable_encoder(ipr_draft)
        update_data = ipr_draft.dict(exclude_unset=True)

        for field in ipr_draft:
            if field in update_data:
                setattr(ipr_obj, field, update_data[field])
        session.add(ipr_obj)
        await session.commit()
        await session.refresh(ipr_obj)
        return HTTPStatus.OK

    async def delete_ipr(self,
                         id_ipr: int,
                         session: AsyncSession,
                         user: User) -> Ipr:
        try:
            db_ipr = await self.get_ipr_by_id(id_ipr)
            self.check_ipr_user(db_ipr, user)
        except HTTPException as exception:
            return {
                "timestamp": datetime.now().isoformat(),
                "status": exception.status_code,
                "error": "Not Found",
                "errorMessage": exception.detail
            }
        await session.delete(db_ipr)
        await session.commit()
        return db_ipr

    async def check_ipr_exists(self,
                               ipr_id: int,
                               session: AsyncSession) -> Ipr:
        ipr = await self.get_ipr_by_id(ipr_id,
                                       session
                                       )
        if ipr is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="ИПР не найден."
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
                               session: AsyncSession,
                               ) -> Optional[str]:

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
            raise HTTPException(HTTPStatus.NOT_FOUND, detail=f'IPR с id - {ipr_id} не существует')

        return ipr

    async def check_ipr_user(self,
                             ipr,
                             user: User):
        if ipr.emplyee_id != user.id or ipr.supervisor_id != user.id:
            raise HTTPException(
                HTTPStatus.FORBIDDEN, detail='У вас нет прав модифицировать/удалять данный ИПР'
            )

ipr_crud = IPRCrud(Ipr)
