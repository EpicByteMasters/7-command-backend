from datetime import date
from typing import Optional

from pydantic import BaseModel, Extra, Field

from app.schemas.base import AllOptional, Base, BaseOut


class TaskStatusOut(BaseOut):
    id: str
    name: str


class TaskFileOut(BaseOut):
    id: int
    name: str
    url_link: str


class EduTaskCreate(BaseModel):
    task_id: int
    education_id: int


class EducationOut(BaseOut):
    id: int
    name: str
    url_link: str


class EduTaskOut(BaseOut):
    status: bool
    education: EducationOut


class FileCreate(BaseModel):
    name: str
    url_link: str
    ipr_id: int


class TaskBase(Base, metaclass=AllOptional):
    name: str
    description: str = Field(None, min_length=1, max_length=96)
    close_date: date


class TaskCreate(TaskBase):
    supervisor_comment: str = Field(None, max_length=96)
    education: list[int]
    ipr_id: int
    comment: str


class TaskUpdate(TaskCreate):
    task_status_id: str


class TaskUpdateSupervisorIn(TaskUpdate):
    id: int


class TaskBase(Base, metaclass=AllOptional):
    name: str
    description: str = Field(None, min_length=1, max_length=96)
    close_date: date


class TaskCreateInput(TaskBase):
    id: int = None
    education: list[int]
    supervisor_comment: str = Field(None, max_length=96)

    class Config:
        extra = Extra.allow


class IPRDraftTaskOut(BaseOut, metaclass=AllOptional):
    id: int
    name: str
    task_status: TaskStatusOut
    description: str
    supervisor_comment: Optional[str]
    close_date: date
    education: list[EduTaskOut]


class IPRTaskOut(IPRDraftTaskOut):
    comment: str
    file: list[TaskFileOut]
