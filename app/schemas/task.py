from datetime import date
from typing import Optional

from pydantic import BaseModel, Extra, Field

from .utils import to_camel


class Educations(BaseModel):
    name: str
    url: Optional[str]


class EduTask(BaseModel):
    status: bool


class EducationsDB(BaseModel):
    id: int
    name: str
    url_link: str

    class Config:
        orm_mode = True
        alias_generator = to_camel
        allow_population_by_field_name = True


class EduTaskCreate(BaseModel):
    task_id: int
    education_id: int


class EduTaskDB(BaseModel):
    status: bool
    education: EducationsDB

    class Config:
        orm_mode = True
        alias_generator = to_camel
        allow_population_by_field_name = True


class FileCreate(BaseModel):
    name: str
    url_link: str
    ipr_id: int


class FileDB(FileCreate):
    id: int

    class Config:
        orm_mode = True
        alias_generator = to_camel
        allow_population_by_field_name = True


class TaskBase(BaseModel):
    name: Optional[str]
    description: Optional[str] = Field(None, min_length=1, max_length=96)
    close_date: Optional[date]


class TaskCreate(TaskBase):
    supervisor_comment: Optional[str] = Field(None, max_length=96)
    education: Optional[list[int]]
    ipr_id: Optional[int]


class TaskStatusDB(BaseModel):
    id: str
    name: str

    class Config:
        orm_mode = True


class TaskDB(TaskBase):
    id: int
    supervisor_comment: Optional[str] = Field(None, max_length=96)
    comment: Optional[str] = Field(None, max_length=96)
    task_status: Optional[TaskStatusDB]
    file: Optional[list[FileDB]]
    education: Optional[list[EduTaskDB]]

    class Config:
        orm_mode = True
        alias_generator = to_camel
        allow_population_by_field_name = True


class TaskCreateInput(TaskBase):
    id: Optional[int] = None
    education: Optional[list[int]]
    supervisor_comment: Optional[str] = Field(None, max_length=96)

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
        extra = Extra.allow
