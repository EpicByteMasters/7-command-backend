from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from app.models.task import Task, Education, EducationTask


class EducationTaskCRUD(CRUDBase):

    async def add_educations(self, obj_in, session: AsyncSession):
        query = select(self.model).where(and_(
            self.model.task_id == obj_in.task_id,
            self.model.education_id == obj_in.education_id))
        result = await session.execute(query)
        result = result.scalar()
        if not result:
            obj = await self.create(obj_in, session)
            return obj
        return result


task_crud = CRUDBase(Task)
education_task_crud = EducationTaskCRUD(EducationTask)
education_crud = CRUDBase(Education)
