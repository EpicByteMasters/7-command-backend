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


class TaskStatus(BaseWithName):
    id = Column(String, primary_key=True)


class TaskFile(BaseWithName):
    url_link = Column(String())


class Task(BaseWithName):
    close_date = Column(Date(), nullable=False)
    description = Column(Text(), nullable=False)
    comment = Column(Text(), nullable=True)
    supervisor_comment = Column(Text(), nullable=True)
    task_status = Column(String, ForeignKey("taskstatus.id"))
    file = Column(Integer, ForeignKey("taskfile.id"), nullable=True)
    ipr_id = Column(Integer, ForeignKey("ipr.id"), nullable=False)


class Education(BaseWithName):
    specialty = Column(String, ForeignKey("specialty.id"))
    url_link = Column(String())


class EducationTask(Base):
    task_id = Column(Integer, ForeignKey("task.id", ondelete="CASCADE"))
    education_id = Column(Integer, ForeignKey("education.id", ondelete="CASCADE"))
    status = Column(Boolean(), server_default=false())


class SpecialtyEducation(Base):
    specialty = Column(String, ForeignKey("specialty.id", ondelete="CASCADE"))
    education_id = Column(Integer, ForeignKey("education.id", ondelete="CASCADE"))


class CompetencyEducation(Base):
    competency = Column(String, ForeignKey("competency.id", ondelete="CASCADE"))
    education_id = Column(Integer, ForeignKey("education.id", ondelete="CASCADE"))
