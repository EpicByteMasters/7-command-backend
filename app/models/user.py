from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Boolean, Column, false, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


from app.core.db import Base, BaseWithName


class Position(BaseWithName):
    id = Column(String, primary_key=True)
    user = relationship("User", back_populates="position", lazy="joined")


class Specialty(BaseWithName):
    id = Column(String, primary_key=True)
    ipr = relationship("Ipr", back_populates="specialty", lazy="joined")
    user = relationship("User", back_populates="specialty", lazy="joined")


class User(SQLAlchemyBaseUserTable[int], Base):
    first_name = Column(String(length=32), nullable=False)
    surname = Column(String(length=64), nullable=False)
    patronymic = Column(String(length=64), nullable=True)
    position_id = Column(String, ForeignKey("position.id"), nullable=True)
    specialty_id = Column(String, ForeignKey("specialty.id"), nullable=True)
    supervisor_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    image_url = Column(String(), nullable=True)
    notifications = relationship("Notification", back_populates="user")
    specialty = relationship("Specialty", back_populates="user", lazy="selectin")
    position = relationship("Position", back_populates="user", lazy="selectin")
    is_mentor = Column(Boolean(), server_default=false())
    is_supervisor = Column(Boolean())
