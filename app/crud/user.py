from app.crud.base import CRUDBase
from app.models import Position, Specialty, User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class CRUDUser(CRUDBase):
    async def get_users_by_boss(self, user: User, session: AsyncSession):
        query = select(self.model).where(self.model.supervisor_id == user.id)
        all_objects = await session.execute(query)
        return all_objects.scalars().all()


position_crud = CRUDBase(Position)
user_crud = CRUDUser(User)
specialty_crud = CRUDBase(Specialty)
