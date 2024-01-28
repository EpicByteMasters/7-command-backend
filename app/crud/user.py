from app.crud.base import CRUDBase
from app.models import Position, Specialty, User

position_crud = CRUDBase(Position)
user_crud = CRUDBase(User)
specialty_crud = CRUDBase(Specialty)
