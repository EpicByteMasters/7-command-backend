from app.crud.base import CRUDBase
from app.models import Specialty, User

user_crud = CRUDBase(User)
specialty_crud = CRUDBase(Specialty)
