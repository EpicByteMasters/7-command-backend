from datetime import date
from typing import Optional

from pydantic import BaseModel, Extra

from .utils import to_camel
from app.schemas.task import TaskCreateInput, TaskDB
from app.schemas.user import SpecialtyDB


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
    employee_id: int
    mentor_id: Optional[int]
    competency: list[CompetencyDB]
    supervisor_id: Optional[int]
    goal: Optional[GoalDB]
    specialty: Optional[SpecialtyDB]
    create_date: Optional[date]
    close_date: Optional[date]
    description: Optional[str]
    supervisor_comment: Optional[str]
    comment: Optional[str]
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
    supervisor_comment: Optional[str]
    tasks: Optional[list[TaskCreateInput]]

    class Config:
        orm_mode = True
        alias_generator = to_camel
        allow_population_by_field_name = True


class IprDraftUpdate(BaseModel):
    goal_id: Optional[str]
    specialty_id: Optional[str]
    mentor_id: Optional[int]
    description: Optional[str]
    supervisor_comment: Optional[str]
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
    competency_id: Optional[list[str]]
    specialty_id: Optional[str]
    mentor_id: Optional[int]
    description: Optional[str]
    supervisor_comment: Optional[str]
    tasks: Optional[list[TaskCreateInput]]
    supervisor_comment: Optional[str]

    class Config:
        alias_generator = to_camel
        allow_population_by_field = True


class FileCreateEmployee(BaseModel):
    name: str
    url_link: str

    class Config:
        extra = Extra.allow
        alias_generator = to_camel
        allow_population_by_field = True


class TaskUpdateEmployee(BaseModel):
    id: int
    comment: str
    file: list[FileCreateEmployee]


class IprUpdateEmployee(BaseModel):
    tasks: Optional[list[TaskUpdateEmployee]]


class IprStatusPatch(BaseModel):
    ipr_status_id: Optional[str]


class IprsOut(BaseModel):
    id: Optional[int]
    first_name: Optional[str]
    last_name: Optional[str]
    middle_name: Optional[str]
    position_id: Optional[str]
    specialty_id: Optional[str]
    image_url: Optional[str]

    goal: Optional[str]
    date_of_end: Optional[str]
    progress: Optional[str]
    task_completed: Optional[int]
    task_count: Optional[int]
    status: Optional[str]
    total_count: Optional[int]

    class Config:
        orm_mode = True
        alias_generator = to_camel
        allow_population_by_field_name = True
