from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text

from app.core.db import Base, BaseWithName


class Goal(BaseWithName):
    pass


class Competency(BaseWithName):
    pass


class Status(BaseWithName):
    pass


class Grade(BaseWithName):
    pass


class CompetencySpecialty(Base):
    specialty_id = Column(Integer, ForeignKey("specialty.id", ondelete="CASCADE"))
    competency_id = Column(Integer, ForeignKey("competency.id", ondelete="CASCADE"))


class CompetencyIpr(Base):
    competency_id = Column(Integer, ForeignKey("competency.id", ondelete="CASCADE"))
    idr_id = Column(Integer, ForeignKey("ipr.id", ondelete="CASCADE"))


class Ipr(Base):
    emplyee_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    supervisor_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    goal_id = Column(Integer, ForeignKey("goal.id"), nullable=True)
    specialty_id = Column(Integer, ForeignKey("specialty.id"), nullable=True)
    create_date = Column(DateTime(), nullable=True)
    close_date = Column(DateTime(), nullable=True)
    mentor_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    description = Column(Text(), nullable=True)
    comment = Column(Text(), nullable=True)
    ipr_status_id = Column(Integer, ForeignKey("status.id"), nullable=False)
    ipr_grade_id = Column(Integer, ForeignKey("grade.id"), nullable=True)
    supervisor_comment = Column(Text(), nullable=True)


class TaskIpr(Base):
    ipr_id = Column(Integer, ForeignKey("ipr.id", ondelete="CASCADE"))
    task_id = Column(Integer, ForeignKey("task.id", ondelete="CASCADE"))
