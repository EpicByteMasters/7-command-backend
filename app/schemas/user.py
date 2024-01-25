from fastapi_users import schemas

from .utils import to_camel


class UserRead(schemas.BaseUser[int]):
    first_name: str
    surname: str
    patronymic: str
    image_url: str
    position_id: int
    specialty_id: int
    supervisor_id: int

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class UserCreate(schemas.BaseUserCreate):
    first_name: str
    surname: str
    patronymic: str
    image_url: str
    position_id: int
    specialty_id: int
    supervisor_id: int
