from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    id: int
    first_name: str
    surname: str
    patronymic: str
    image_url: str
    position_id: int
    specialty_id: int
    supervisor_id: int


class UserCreate(schemas.BaseUserCreate):
    first_name: str
    surname: str
    patronymic: str
    image_url: str
    position_id: int
    specialty_id: int
    supervisor_id: int
