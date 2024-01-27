from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from app.models.task import Task, Education, EducationTask


class TaskCrud(CRUDBase):

    async def patch_task_awaiting_review(
            self,
            task_id: int,
            session: AsyncSession,
    ) -> Optional[Task]:
        task = await task_crud.get(task_id, session=session)
        task.task_status = "AWAITING_REVIEW"
        session.add(task)
        await session.commit()
        await session.refresh(task)

        return task


task_crud = TaskCrud(Task)
education_task_crud = CRUDBase(EducationTask)
education_crud = CRUDBase(Education)
