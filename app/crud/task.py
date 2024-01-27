from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task import Task, Education, EducationTask


class CRUDTask(CRUDBase):

    async def get_multi_task_by_iprid(self, ipr_id: int, session: AsyncSession):
        query = select(self.model).where(self.model.ipr_id == ipr_id)
        all_objects = await session.execute(query)
        return all_objects.scalars().all()


task_crud = CRUDTask(Task)
education_task_crud = CRUDBase(EducationTask)
education_crud = CRUDBase(Education)
