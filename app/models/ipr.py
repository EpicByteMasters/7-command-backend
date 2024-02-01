from datetime import date

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    event,
    false,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from app.core.db import Base, BaseWithName


class Goal(BaseWithName):
    id = Column(String, primary_key=True)
    ipr = relationship("Ipr")


class Competency(BaseWithName):
    id = Column(String, primary_key=True)
    skill_type = Column(String())
    ipr = relationship("CompetencyIpr")


class Status(BaseWithName):
    id = Column(String, primary_key=True)
    ipr = relationship("Ipr")


class CompetencySpecialty(Base):
    id = Column(Integer(), nullable=True)
    specialty = Column(
        String, ForeignKey("specialty.id", ondelete="CASCADE"), primary_key=True
    )
    competency = Column(
        String, ForeignKey("competency.id", ondelete="CASCADE"), primary_key=True
    )


class CompetencyIpr(Base):
    id = Column(Integer(), nullable=True)
    competency = Column(String,
                        ForeignKey("competency.id", ondelete="CASCADE"),
                        primary_key=True)
    ipr_id = Column(Integer,
                    ForeignKey("ipr.id", ondelete="CASCADE"),
                    primary_key=True)
    ipr_rel = relationship("Ipr")
    competency_rel = relationship("Competency",
                                  back_populates="ipr",
                                  lazy="joined")


class Ipr(Base):
    employee_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    supervisor_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    goal_id = Column(String, ForeignKey("goal.id"), nullable=True)
    specialty_id = Column(String, ForeignKey("specialty.id"), nullable=True)
    create_date = Column(Date(), nullable=True)
    close_date = Column(Date(), nullable=True)
    mentor_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    description = Column(Text(length=96), nullable=True)
    comment = Column(Text(length=96), nullable=True)
    ipr_status_id = Column(String, ForeignKey("status.id"), nullable=False)
    ipr_grade = Column(Integer(), nullable=True)
    supervisor_comment = Column(Text(), nullable=True)
    is_deleted = Column(Boolean(), server_default=false())
    notifications = relationship("Notification", back_populates="ipr")
    task = relationship("Task", back_populates="ipr", lazy="joined")
    goal = relationship("Goal", back_populates="ipr", lazy="joined")
    specialty = relationship("Specialty", back_populates="ipr", lazy="joined")
    status = relationship("Status", back_populates="ipr", lazy="joined")
    competency = relationship("CompetencyIpr",
                              back_populates="ipr_rel",
                              lazy="joined")
    mentor = relationship("User",
                          foreign_keys=[mentor_id],
                          primaryjoin="Ipr.mentor_id == User.id",
                          lazy="joined")
    task_completed = Column(Integer(), default=0)

    @hybrid_property
    def task_count(self):
        return len(self.task)


@event.listens_for(Ipr.ipr_status_id, "set")
def create_date_set_when_status_in_progress(target, value, oldvalue, initiator):
    if value != "DRAFT":
        target.create_date = date.today()
