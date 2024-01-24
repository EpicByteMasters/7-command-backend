from .base import CRUDBase
from app.models.task import Task, Education, EducationTask

task_crud = CRUDBase(Task)
education_task_crud = CRUDBase(EducationTask)
education_crud = CRUDBase(Education)
