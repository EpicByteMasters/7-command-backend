from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, func

from app.core.db import Base, BaseWithName


class Goal(BaseWithName):
    pass


class Competency(BaseWithName):
    skill_type = Column(Integer())


class Status(BaseWithName):
    pass


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
    create_date = Column(DateTime(), func.now, nullable=True)
    close_date = Column(DateTime(), nullable=True)
    mentor_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    description = Column(Text(), nullable=True)
    comment = Column(Text(), nullable=True)
    ipr_status_id = Column(Integer, ForeignKey("status.id"), nullable=False)
    ipr_grade = Column(Integer(), nullable=True)
    supervisor_comment = Column(Text(), nullable=True)
