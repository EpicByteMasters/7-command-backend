from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    false,
    ForeignKey,
    Integer,
    String,
    Text,
)

from app.core.db import Base, BaseWithName


class TaskStatus(BaseWithName):
    pass


class TaskFile(BaseWithName):
    url_link = Column(String())


class Task(BaseWithName):
    close_date = Column(DateTime())
    description = Column(Text())
    comment = Column(Text(), nullable=True)
    supervisor_comment = Column(Text(), nullable=True)
    task_status_id = Column(Integer, ForeignKey("taskstatus.id"))
    file = Column(Integer, ForeignKey("taskfile.id"))


class Education(BaseWithName):
    competency_id = Column(Integer, ForeignKey("competency.id", ondelete="CASCADE"))
    specialty_id = Column(Integer, ForeignKey("specialty.id", ondelete="CASCADE"))
    url_link = Column(String())


class EducationTask(Base):
    task_id = Column(Integer, ForeignKey("task.id", ondelete="CASCADE"))
    education_id = Column(Integer, ForeignKey("education.id", ondelete="CASCADE"))
    status = Column(Boolean(), server_default=false())


class SpecialtyEducation(Base):
    specialty_id = Column(Integer, ForeignKey("specialty.id", ondelete="CASCADE"))
    education_id = Column(Integer, ForeignKey("education.id", ondelete="CASCADE"))


class CompetencyLearning(Base):
    competency_id = Column(Integer, ForeignKey("competency.id", ondelete="CASCADE"))
    education_id = Column(Integer, ForeignKey("education.id", ondelete="CASCADE"))
