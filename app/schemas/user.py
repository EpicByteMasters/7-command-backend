from datetime import date

from fastapi_users import schemas
from pydantic import BaseModel

from .utils import to_camel


class IprStatusDB(BaseModel):
    name: str

    class Config:
        orm_mode = True


class IprGoalDB(IprStatusDB):
    pass


class SpecialtyDB(BaseModel):
    name: str

    class Config:
        orm_mode = True


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

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class IprInUserRead(BaseModel):
    id: int
    goal: IprGoalDB
    close_date: date
    status: IprStatusDB


class UserIprListRead(BaseModel):
    first_name: str
    surname: str
    patronymic: str
    image_url: str
    specialty: SpecialtyDB
    ipr_employee: IprInUserRead

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


class UserMentorIpr(BaseModel):
    name: str
    surname: str
    patronymic: str
