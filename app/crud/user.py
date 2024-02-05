from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Ipr, Position, Specialty, User


class CRUDUser(CRUDBase):

    async def is_mentor(self, user_id: int, session: AsyncSession):
        query = (
            select(Ipr.id)
            .where(Ipr.ipr_status_id == "IN_PROGRESS",
                   Ipr.mentor_id == user_id)
        )
        ipr = await session.execute(query)
        ipr = ipr.scalar()
        if ipr is None:
            return False
        return True

    async def check_user_exists(self, user_id, session: AsyncSession):
        user = await self.get(user_id, session)
        if user is None:
            return None
        return user

    async def get_users_by_boss(self, user: User, session: AsyncSession):
        query = select(self.model).where(
            self.model.supervisor_id == user.id
        )
        all_objects = await session.execute(query)
        return all_objects.scalars().all()


position_crud = CRUDBase(Position)
user_crud = CRUDUser(User)
specialty_crud = CRUDBase(Specialty)
