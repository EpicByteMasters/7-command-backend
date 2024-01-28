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


task_status_crud = CRUDBase(TaskStatus)
task_crud = CRUDBase(Task)
education_task_crud = EducationTaskCRUD(EducationTask)
education_crud = CRUDBase(Education)
