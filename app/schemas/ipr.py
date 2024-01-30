from datetime import date
from typing import Optional

from pydantic import BaseModel

from .utils import to_camel
from app.schemas.task import TaskCreateInput, TaskDB
from app.schemas.user import SpecialtyDB, UserMentorIpr


class StatusDB(BaseModel):
    id: str
    name: str

    class Config:
        orm_mode = True


class GoalDB(StatusDB):
    pass


class CompetencyRel(StatusDB):
    pass


class CompetencyDB(BaseModel):
    competency_rel: CompetencyRel

    class Config:
        orm_mode = True


class IprDraftDB(BaseModel):
    id: int
    status: StatusDB
    competency: list[CompetencyDB]
    supervisor_id: Optional[int]
    goal: Optional[GoalDB]
    specialty: Optional[SpecialtyDB]
    create_date: Optional[date]
    close_date: Optional[date]
    mentor: Optional[UserMentorIpr]
    description: Optional[str]
    comment: Optional[str]
    supervisor_comment: Optional[str]
    task: Optional[list[TaskDB]]

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

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class IprListRead(BaseModel):
    id: int
    goal: Optional[GoalDB]
    status: StatusDB
    create_date: Optional[date]
    close_date: Optional[date]

    class Config:
        orm_mode = True
        alias_generator = to_camel
        allow_population_by_field_name = True


class IprDraftUpdateInput(BaseModel):
    goal_id: Optional[str]
    specialty_id: Optional[str]
    competency: Optional[list[str]]
    mentor_id: Optional[int]
    description: Optional[str]
    comment: Optional[str]
    tasks: Optional[list[TaskCreateInput]]

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True

    # @validator("comment")
    # def text_does_not_have_incorrect_symbols(cls, value):
    #     pattern = re.compile(r'^[a-zA-Zа-яА-ЯёЁ0-9]+$')
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


class IprDraftUpdate(BaseModel):
    goal_id: Optional[str]
    specialty_id: Optional[str]
    mentor_id: Optional[int]
    description: Optional[str]
    comment: Optional[str]
    ipr_status_id: Optional[str]


class TaskIprCreate(BaseModel):
    ipr_id: int
    task_id: int


class CompetencyIprCreate(BaseModel):
    competency: str
    ipr_id: int


class IprUpdate(BaseModel):
    ipr_status_id: Optional[str]
    goal_id: Optional[str]
    competency: Optional[list[str]]
    specialty_id: Optional[str]
    mentor_id: Optional[int]
    description: Optional[str]
    comment: Optional[str]
    tasks: Optional[list[TaskCreateInput]]
    supervisor_comment: Optional[str]


class IprStatusPatch(BaseModel):
    ipr_status_id: Optional[str]
