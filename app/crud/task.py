from typing import Optional

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from app.models.task import (
    Education,
    EducationTask,
    Task,
    TaskStatus,
    TaskFile
)


class EducationTaskCRUD(CRUDBase):

    async def get_or_create(self,
                            edu_id,
                            task_id,
                            schema,
                            session: AsyncSession):
        query = (
            select(EducationTask)
            .where(EducationTask.education_id == edu_id,
                   EducationTask.task_id == task_id)
        )
        result = await session.execute(query)
        result = result.scalar()
        if result is not None:
            return
        obj = self.create(schema, session)
        return obj

    async def get_object_by_task_and_edu_id(self,
                                            task_id,
                                            edu_id,
                                            session: AsyncSession):
        query = (
            select(EducationTask)
            .where(EducationTask.education_id == edu_id,
                   EducationTask.task_id == task_id)
        )
        result = await session.execute(query)
        result = result.unique().scalar()
        return result


class TaskCrud(CRUDBase):
    async def patch_task_awaiting_review(
        self,
        task_id: int,
        session: AsyncSession,
    ) -> Optional[Task]:
        task = await task_crud.get(task_id, session=session)
        task.task_status_id = "AWAITING_REVIEW"
        session.add(task)
        await session.commit()
        await session.refresh(task)

        return task

    async def check_task_in_ipr(self,
                                task_id: int,
                                ipr_id: int,
                                session: AsyncSession):
        query = (
            select(Task)
            .where(and_(Task.id == task_id, Task.ipr_id == ipr_id))
        )
        result = await session.execute(query)
        result = result.scalar()
        return result

    async def get_multi_task_by_iprid(self, ipr_id: int, session: AsyncSession):
        query = select(self.model).where(self.model.ipr_id == ipr_id)
        all_objects = await session.execute(query)
        return all_objects.unique().scalars().all()


task_crud = TaskCrud(Task)
file_crud = CRUDBase(TaskFile)
task_status_crud = CRUDBase(TaskStatus)
education_task_crud = EducationTaskCRUD(EducationTask)
education_crud = CRUDBase(Education)
