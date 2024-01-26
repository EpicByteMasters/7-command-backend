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
    id = Column(String, primary_key=True)


class Competency(BaseWithName):
    id = Column(String, primary_key=True)
    skill_type = Column(String())


class Status(BaseWithName):
    id = Column(String, primary_key=True)


class CompetencySpecialty(Base):
    specialty = Column(String, ForeignKey("specialty.id", ondelete="CASCADE"))
    competency = Column(String, ForeignKey("competency.id", ondelete="CASCADE"))


class CompetencyIpr(Base):
    competency = Column(String, ForeignKey("competency.id", ondelete="CASCADE"))
    ipr_id = Column(Integer, ForeignKey("ipr.id", ondelete="CASCADE"))


class Ipr(Base):
    employee_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    supervisor_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    goal = Column(String, ForeignKey("goal.id"), nullable=True)
    specialty = Column(String, ForeignKey("specialty.id"), nullable=True)
    create_date = Column(Date(), nullable=True)
    close_date = Column(Date(), nullable=True)
    mentor_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    description = Column(Text(), nullable=True)
    comment = Column(Text(), nullable=True)
    ipr_status = Column(String, ForeignKey("status.id"), nullable=False)
    ipr_grade = Column(Integer(), nullable=True)
    supervisor_comment = Column(Text(), nullable=True)
    is_deleted = Column(Boolean(), server_default=false())
