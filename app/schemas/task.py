from datetime import date
from typing import Optional

from pydantic import BaseModel, Field

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
    url: str


class FileDB(FileCreate):
    id: int

    class Config:
        orm_mode = True


class TaskBase(BaseModel):
    name: str
    description: str = Field(..., min_length=1, max_length=96)
    close_date: Optional[date]

    # @validator("description")
    # def text_does_not_have_incorrect_symbols(cls, value):
    #     pattern = re.compile(r'^[а-яА-ЯёЁa-zA-Z0-9?.,!:-_*()%"]+$')
    #     if not pattern.match(value):
    #         raise ValueError("Использованы некорректные символы")
    #     return value

    # @validator("close_date")
    # def close_date_bigger_than_now(cls, value):
    #     time_now = date.today()
    #     if value <= time_now:
    #         raise ValueError(
    #             "Дата окончания ИПР не должна быть меньше или равна текущей дате"
    #         )
    #     return value


class TaskDB(TaskBase):
    id: int
    supervisor_comment: Optional[str] = Field(None, max_length=96)
    comment: Optional[str] = Field(None, max_length=96)
    status: Optional[str]
    file: Optional[list[FileDB]]
    education: Optional[list[EduTaskDB]]

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
        orm_mode = True


class TaskCreateInput(TaskBase):
    educations: Optional[list[int]]
    supervisor_comment: Optional[str] = Field(None, max_length=96)
    status: Optional[str] = "IN_PROGRESS"

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True

    # @validator("supervisor_comment")
    # def text_does_not_have_incorrect_symbols(cls, value):
    #     pattern = re.compile(r'^[a-zA-Zа-яА-ЯёЁ0-9]+$')
    #     if not pattern.match(value):
    #         return value
    #         # raise ValueError("Использованы некорректные символы")
    #     return value


class TaskCreate(TaskBase):
    supervisor_comment: Optional[str] = Field(None, max_length=96)
    ipr_id: int
