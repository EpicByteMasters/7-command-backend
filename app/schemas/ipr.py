import re
from datetime import date
from typing import Optional

from pydantic import BaseModel, validator

from app.schemas.task import TaskCreateInput, TaskDB


class IprDraftReturn(BaseModel):
    id: int
    ipr_status_id: int

    class Config:
        orm_mode = True


class IprDraftCreate(BaseModel):
    employee_id: int
    supervisor_id: Optional[int]
    ipr_status_id: Optional[int]


class IprDraftUpdateInput(BaseModel):
    goal: Optional[str]
    specialty: Optional[str]
    competence: Optional[list[str]]
    close_date: Optional[date]
    mentor_id: Optional[int]
    description: Optional[str]
    comment: Optional[str]
    tasks: Optional[list[TaskCreateInput]]
    ipr_status_id: int

    @validator("comment")
    def text_does_not_have_incorrect_symbols(cls, value):
        pattern = re.compile(r'^[а-яА-ЯёЁa-zA-Z0-9?.,!:-_*()%"]+$')
        if not pattern.match(value):
            raise ValueError("Использованы некорректные символы")
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
    goal_id: Optional[int]
    specialty_id: Optional[int]
    close_date: Optional[date]
    mentor_id: Optional[int]
    description: Optional[str]
    comment: Optional[str]
    ipr_status_id: Optional[int]


class TaskIprCreate(BaseModel):
    ipr_id: int
    task_id: int


class CompetencyIprCreate(BaseModel):
    competency_id: int
    ipr_id: int


class IprPut(BaseModel):
    mentorId: Optional[int]
    comment: Optional[str]
    tasks: Optional[list[TaskDB]]
