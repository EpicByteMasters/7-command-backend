from datetime import date
from typing import Optional

from pydantic import BaseModel, Extra, Field

from .utils import to_camel


class Base(BaseModel):

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class BaseOut(Base):

    class Config:
        orm_mode = True


class IPRStatusOut(BaseOut):
    id: str
    name: str


class IPRGoalOut(IPRStatusOut):
    pass


class IPRSpecialtyOut(IPRStatusOut):
    pass


class CompetencyRel(IPRStatusOut):
    pass


class TaskStatusOut(IPRStatusOut):
    pass


class IPRCompetencyOut(BaseOut):
    competency_rel: CompetencyRel


class IPRDraftCreate(Base):
    employee_id: int


class IPRDraftCreateOut(BaseOut):
    id: int
    employee_id: int
    supervisor_id: int
    status: IPRStatusOut


class IprListOut(BaseOut):
    id: int
    goal: IPRGoalOut
    status: IPRStatusOut
    create_date: date
    close_date: date


class TaskFileOut(BaseOut):
    id: int
    name: str
    url_link: str
    # ipr_id: str


class EducationOut(BaseOut):
    id: int
    name: str
    url_link: str


class EduTaskOut(BaseOut):
    status: bool
    education: EducationOut


class IPRDraftTaskOut(BaseOut):
    id: int
    name: str
    task_status: TaskStatusOut
    description: str
    supervisor_comment: Optional[str]
    close_date: date
    file: Optional[list[TaskFileOut]]
    education: Optional[list[EduTaskOut]]


class IPRDraftOut(BaseOut):
    id: int
    employee_id: int
    supervisor_id: int
    mentor_id: Optional[int]
    status: IPRStatusOut
    goal: Optional[IPRGoalOut]
    specialty: Optional[IPRSpecialtyOut]
    competency: Optional[list[IPRCompetencyOut]]
    description: Optional[str]
    supervisor_comment: Optional[str]
    task: Optional[list[IPRDraftTaskOut]]


class TaskBase(BaseModel):
    name: Optional[str]
    description: Optional[str] = Field(None, min_length=1, max_length=96)
    close_date: Optional[date]


class TaskCreateInput(TaskBase):
    id: Optional[int] = None
    education: Optional[list[int]]
    supervisor_comment: Optional[str] = Field(None, max_length=96)

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
        extra = Extra.allow


class IPRDraftIn(Base):
    goal_id: Optional[str]
    specialty_id: Optional[str]
    competency: Optional[list[str]]
    mentor_id: Optional[int]
    description: Optional[str]
    supervisor_comment: Optional[str]
    tasks: Optional[list[TaskCreateInput]]


class IPRTaskOut(IPRDraftTaskOut):
    comment: Optional[str]


class IPREmployeeOut(BaseOut):
    id: int
    employee_id: int
    supervisor_id: int
    mentor_id: Optional[int]
    status: IPRStatusOut
    goal: IPRGoalOut
    specialty: IPRSpecialtyOut
    competency: list[IPRCompetencyOut]
    description: Optional[str]
    task: list[IPRTaskOut]
    comment: Optional[str]


class IPRSupervisorOut(BaseOut):
    id: int
    employee_id: int
    supervisor_id: int
    mentor_id: Optional[int]
    status: IPRStatusOut
    goal: IPRGoalOut
    specialty: IPRSpecialtyOut
    competency: list[IPRCompetencyOut]
    description: Optional[str]
    supervisor_comment: Optional[str]
    task: list[IPRTaskOut]
    comment: Optional[str]
