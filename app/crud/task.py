from typing import Optional

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from app.models.task import Education, EducationTask, Task, TaskStatus


class EducationTaskCRUD(CRUDBase):

    async def remove_all_educations_from_task(self, task_id, session: AsyncSession):
        query = delete(EducationTask).where(EducationTask.task_id == task_id)
        await session.execute(query)
        await session.commit()
        return


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
task_status_crud = CRUDBase(TaskStatus)
education_task_crud = EducationTaskCRUD(EducationTask)
education_crud = CRUDBase(Education)
