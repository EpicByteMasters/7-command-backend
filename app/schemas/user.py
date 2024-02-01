from datetime import date
from typing import Optional

from fastapi_users import schemas
from pydantic import BaseModel

from .utils import to_camel


class IprStatusDB(BaseModel):
    id: str
    name: str

    class Config:
        orm_mode = True


class IprGoalDB(IprStatusDB):
    pass


class SpecialtyDB(IprStatusDB):
    pass


class PositionDB(SpecialtyDB):
    pass


class UserRead(schemas.BaseUser[int]):
    first_name: str
    surname: str
    patronymic: str
    image_url: str
    position: PositionDB
    specialty: SpecialtyDB
    supervisor_id: int
    is_supervisor: bool
    is_mentor: bool

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class IprInUserRead(BaseModel):
    id: int
    goal: IprGoalDB
    close_date: date
    status: IprStatusDB
    is_supervisor: bool


class UserIprListRead(BaseModel):
    first_name: str
    surname: str
    patronymic: str
    image_url: str
    specialty: SpecialtyDB
    ipr_employee: IprInUserRead
    is_supervisor: bool

    class Config:
        orm_mode = True
        alias_generator = to_camel
        allow_population_by_field_name = True


class UserCreate(schemas.BaseUserCreate):
    first_name: str
    surname: str
    patronymic: str
    image_url: str
    position_id: str
    specialty_id: str
    supervisor_id: int
    is_supervisor: bool


class UserUpdate(schemas.BaseUserUpdate):
    first_name: Optional[str]
    surname: Optional[str]
    patronymic: Optional[str]
    image_url: Optional[str]
    supervisor_id: Optional[int]
    position_id: Optional[str]
    specialty_id: Optional[str]
    is_mentor: Optional[bool]
    is_supervisor: Optional[bool]


class UserMentorIpr(BaseModel):
    name: str
    surname: str
    patronymic: str
