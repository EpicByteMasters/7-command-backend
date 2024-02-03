from datetime import date
from typing import Optional

from pydantic import BaseModel, Extra, Field

from app.schemas.task import IPRDraftTaskOut, IPRTaskOut

from .base import AllOptional, Base, BaseOut


class CompetencyIprCreate(BaseModel):
    competency: str
    ipr_id: int


class IPRStatusOut(BaseOut):
    id: str
    name: str


class IPRGoalOut(IPRStatusOut):
    pass


class IPRSpecialtyOut(IPRStatusOut):
    pass


class CompetencyRel(IPRStatusOut):
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
    task_count: int
    task_completed: int


class IprListSupervisorOut(BaseOut):
    id: int
    goal: Optional[IPRGoalOut]
    status: IPRStatusOut
    create_date: Optional[date]
    close_date: Optional[date]
    task_count: int
    task_completed: int


class UserMentorOut(BaseOut):
    id: int
    first_name: str
    surname: str
    patronymic: str
    image_url: str


class IPRDraftOut(BaseOut):
    id: int
    employee_id: int
    supervisor_id: int
    mentor: Optional[UserMentorOut]
    status: IPRStatusOut
    goal: Optional[IPRGoalOut]
    specialty: Optional[IPRSpecialtyOut]
    competency: Optional[list[IPRCompetencyOut]]
    description: Optional[str]
    supervisor_comment: Optional[str]
    task: Optional[list[IPRDraftTaskOut]]


class TaskBase(Base, metaclass=AllOptional):  #
    name: str
    description: str = Field(None, min_length=1, max_length=96)
    close_date: date


class TaskCreateInput(TaskBase):  #
    id: int = None
    education: list[int]
    supervisor_comment: str = Field(None, max_length=96)

    class Config:
        extra = Extra.allow


class IPRDraftUpdate(Base, metaclass=AllOptional):
    goal_id: str
    specialty_id: str
    mentor_id: int
    description: str
    supervisor_comment: str
    ipr_status_id: str


class IPRDraftIn(IPRDraftUpdate):
    competency: list[str]
    tasks: list[TaskCreateInput]


class IPREmployeeOut(BaseOut):
    id: int
    employee_id: int
    supervisor_id: int
    mentor: Optional[UserMentorOut]
    create_date: date
    close_date: date
    status: IPRStatusOut
    goal: IPRGoalOut
    specialty: IPRSpecialtyOut
    competency: list[IPRCompetencyOut]
    description: Optional[str]
    task: list[IPRTaskOut]
    comment: Optional[str]
    ipr_grade: Optional[int]


class IPRSupervisorOut(BaseOut, metaclass=AllOptional):
    id: int
    employee_id: int
    supervisor_id: int
    mentor: UserMentorOut
    status: IPRStatusOut
    goal: IPRGoalOut
    specialty: IPRSpecialtyOut
    competency: list[IPRCompetencyOut]
    description: str
    supervisor_comment: str
    task: list[IPRTaskOut]
    comment: str
    ipr_grade: int


class IprUpdateSupervisorIn(Base, metaclass=AllOptional):
    goal_id: str
    competency: list[str]
    specialty_id: str
    mentor_id: int
    description: str
    tasks: list[TaskCreateInput]
    supervisor_comment: str


class FileCreateEmployeeIn(Base):
    name: str
    url_link: str

    class Config:
        extra = Extra.allow


class TaskUpdateEmployeeIn(Base):
    id: int
    comment: Optional[str]
    file: Optional[list[FileCreateEmployeeIn]]


class IprUpdateEmployeeIn(Base):
    tasks: Optional[list[TaskUpdateEmployeeIn]]


class IprComplete(Base):
    ipr_status: str
    ipr_grade: int
    supervisor_comment: str


class IprsOut(BaseModel):
    id: Optional[int]
    first_name: Optional[str]
    last_name: Optional[str]
    middle_name: Optional[str]
    position_id: Optional[str]

    ipr_id: Optional[int]
    goal_id: Optional[str]
    date_of_end: Optional[str]
    task_completed: Optional[int]
    task_count: Optional[int]
    status_id: Optional[str]
    total_count_iprs: Optional[int]
    total_count_employees: Optional[int]
