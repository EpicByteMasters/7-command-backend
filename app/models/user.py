from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.db import Base, BaseWithName


class Position(BaseWithName):
    pass


class Specialty(BaseWithName):
    pass


class User(SQLAlchemyBaseUserTable[int], Base):
    first_name = Column(String(length=32), nullable=False)
    surname = Column(String(length=64), nullable=False)
    patronymic = Column(String(length=64), nullable=True)
    position_id = Column(Integer, ForeignKey('position.id'))
    specialty_id = Column(Integer, ForeignKey('specialty.id'))
    supervisor_id = Column(Integer, ForeignKey('user.id'), index=True)
    supervisor = relationship(
        lambda: User, remote_side=id, backref='supervisor')
    image_url = Column(String())
