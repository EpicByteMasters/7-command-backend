from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, ForeignKey, Integer, String


from app.core.db import Base, BaseWithName


class Position(BaseWithName):
    pass


class Specialty(BaseWithName):
    pass


class User(SQLAlchemyBaseUserTable[int], Base):
    first_name = Column(String(length=32), nullable=False)
    surname = Column(String(length=64), nullable=False)
    patronymic = Column(String(length=64), nullable=True)
    position_id = Column(Integer, ForeignKey("position.id"), nullable=True)
    specialty_id = Column(Integer, ForeignKey("specialty.id"), nullable=True)
    supervisor_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    image_url = Column(String(), nullable=True)