from sqlalchemy import (
    Boolean,
    Column,
    Date,
    false,
    ForeignKey,
    Integer,
    String,
    Text,
)

from app.core.db import Base, BaseWithName


class Goal(BaseWithName):
    pass


class Competency(BaseWithName):
    skill_type = Column(Integer())


class Status(Base):
    id = Column(String, primary_key=True)
    name = Column(String())


class CompetencySpecialty(Base):
    specialty_id = Column(Integer, ForeignKey("specialty.id", ondelete="CASCADE"))
    competency_id = Column(Integer, ForeignKey("competency.id", ondelete="CASCADE"))


class CompetencyIpr(Base):
    competency_id = Column(Integer, ForeignKey("competency.id", ondelete="CASCADE"))
    ipr_id = Column(Integer, ForeignKey("ipr.id", ondelete="CASCADE"))


class Ipr(Base):
    employee_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    supervisor_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    goal_id = Column(Integer, ForeignKey("goal.id"), nullable=True)
    specialty_id = Column(Integer, ForeignKey("specialty.id"), nullable=True)
    create_date = Column(Date(), nullable=True)
    close_date = Column(Date(), nullable=True)
    mentor_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    description = Column(Text(), nullable=True)
    comment = Column(Text(), nullable=True)
    ipr_status_id = Column(String, ForeignKey("status.id"), nullable=False)
    ipr_grade = Column(Integer(), nullable=True)
    supervisor_comment = Column(Text(), nullable=True)
    is_deleted = Column(Boolean(), server_default=false())
