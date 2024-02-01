from sqlalchemy import (
    Boolean,
    Column,
    Date,
    false,
    ForeignKey,
    Integer,
    String,
    Text,
    Date,
)
from sqlalchemy.orm import relationship

from app.core.db import Base, BaseWithName


class TaskStatus(BaseWithName):
    id = Column(String, primary_key=True)
    task = relationship("Task")


class TaskFile(BaseWithName):
    url_link = Column(String())
    ipr_id = Column(Integer, ForeignKey("task.id", ondelete="CASCADE"))
    task = relationship("Task")


class EducationTask(Base):
    id = Column(Integer(), nullable=True)
    task_id = Column(
        Integer, ForeignKey("task.id", ondelete="CASCADE"), primary_key=True
    )
    education_id = Column(
        Integer,
        ForeignKey("education.id", ondelete="CASCADE"),
        primary_key=True,
    )
    status = Column(Boolean(), server_default=false())
    education = relationship("Education", back_populates="task", lazy="selectin")
    task = relationship("Task", back_populates="education", lazy="selectin")


class Task(BaseWithName):
    close_date = Column(Date(), nullable=True)
    description = Column(Text(), nullable=True)
    comment = Column(Text(length=96), nullable=True)
    supervisor_comment = Column(Text(length=96), nullable=True)
    task_status_id = Column(String,
                            ForeignKey("taskstatus.id"),
                            default="IN_PROGRESS")
    ipr_id = Column(Integer,
                    ForeignKey("ipr.id", ondelete="CASCADE"),
                    nullable=False)
    ipr = relationship("Ipr", back_populates="task")
    education = relationship("EducationTask",
                             back_populates="task",
                             lazy="joined")
    file = relationship("TaskFile", back_populates="task", lazy="joined")
    task_status = relationship("TaskStatus", back_populates="task", lazy="joined")
    notifications = relationship("Notification", back_populates="task")


class Education(BaseWithName):
    specialty = Column(String, ForeignKey("specialty.id"))
    url_link = Column(String())
    task = relationship("EducationTask", back_populates="education", lazy="selectin")


class SpecialtyEducation(Base):
    id = Column(Integer(), nullable=True)
    specialty = Column(
        String, ForeignKey("specialty.id", ondelete="CASCADE"), primary_key=True
    )
    education_id = Column(
        Integer, ForeignKey("education.id", ondelete="CASCADE"), primary_key=True
    )


class CompetencyEducation(Base):
    id = Column(Integer(), nullable=True)
    competency = Column(
        String, ForeignKey("competency.id", ondelete="CASCADE"), primary_key=True
    )
    education_id = Column(
        Integer, ForeignKey("education.id", ondelete="CASCADE"), primary_key=True
    )
