import re
from datetime import date
from typing import Optional

from pydantic import BaseModel, validator

from .utils import to_camel
from app.schemas.task import TaskCreateInput, TaskDB


class IprDB(BaseModel):
    id: int
    ipr_status: str
    supervisor_id: Optional[int]
    goal: Optional[str]
    specialty: Optional[str]
    create_date: Optional[date]
    close_date: Optional[date]
    mentor_id: Optional[int]
    description: Optional[str]
    comment: Optional[str]
    supervisor_comment: Optional[str]

    class Config:
        orm_mode = True
        alias_generator = to_camel
        allow_population_by_field_name = True


class IprWorkerGet(BaseModel):
    goal: str
    specialty: str
    create_date: Optional[date]
    close_date: Optional[date]
    mentor_id: Optional[int]
    description: Optional[str]
    comment: Optional[str]
    tasks: Optional[list[TaskDB]]
    ipr_status: str


class IprListRead(BaseModel):
    id: int
    goal: str
    ipr_status: str
    create_date: date
    close_date: date

    class Config:
        orm_mode = True
        alias_generator = to_camel
        allow_population_by_field_name = True


class IprDraftCreate(BaseModel):
    employee_id: int
    supervisor_id: Optional[int]
    ipr_status: Optional[str]

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class IprDraftUpdateInput(BaseModel):
    goal: Optional[str]
    specialty: Optional[str]
    competence: Optional[list[str]]
    close_date: Optional[date]
    mentor_id: Optional[int]
    description: Optional[str]
    comment: Optional[str]
    tasks: Optional[list[TaskCreateInput]]
    ipr_status: str

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True

    @validator("comment")
    def text_does_not_have_incorrect_symbols(cls, value):
        pattern = re.compile(r'^[a-zA-Zа-яА-ЯёЁ0-9]+$')
        if not pattern.match(value):
            return value
            # raise ValueError("Использованы некорректные символы")
        return value

    @validator("close_date")
    def close_date_bigger_than_now(cls, value):
        time_now = date.today()
        if value <= time_now:
            raise ValueError(
                "Дата окончания ИПР не должна быть меньше или равна текущей дате"
            )
        return value


class IprDraftUpdate(BaseModel):
    goal: Optional[str]
    specialty: Optional[str]
    close_date: Optional[date]
    mentor_id: Optional[int]
    description: Optional[str]
    comment: Optional[str]
    ipr_status: Optional[str]


class TaskIprCreate(BaseModel):
    ipr_id: int
    task_id: int


class CompetencyIprCreate(BaseModel):
    competency: str
    ipr_id: int
