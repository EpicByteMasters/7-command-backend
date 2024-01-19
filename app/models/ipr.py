from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text

from app.core.db import Base, BaseWithName


class Goal(BaseWithName):  # ready to use
    pass


class Competency(BaseWithName):  # ready to use
    pass


class Status(BaseWithName):  # ready to use
    pass


class Grade(BaseWithName):  # ready to use
    pass


class CompetencySpecialty(Base):  # ready to use
    specialty_id = Column(
        Integer,
        ForeignKey('specialty.id', ondelete='CASCADE')
    )
    competency_id = Column(
        Integer,
        ForeignKey('competency.id', ondelete='CASCADE')
    )


class CompetencyIpr(Base):  # ready to use
    competency_id = Column(
        Integer,
        ForeignKey('competency.id', ondelete='CASCADE')
    )
    idr_id = Column(
        Integer,
        ForeignKey('ipr.id', ondelete='CASCADE')
    )


class Ipr(Base):
    emplyee_id = Column(Integer, ForeignKey('user.id'))
    supervisor_id = Column(Integer, ForeignKey('user.id'))
    goal_id = Column(Integer, ForeignKey('goal.id'))
    specialty_id = Column(Integer, ForeignKey('specialty.id'))
    create_date = Column(DateTime())
    close_date = Column(DateTime())
    mentor_id = Column(Integer, ForeignKey('user.id'))
    description = Column(Text())
    comment = Column(Text())
    ipr_status_id = Column(Integer, ForeignKey('status.id'))
    ipr_grade_id = Column(Integer, ForeignKey('grade.id'))
    supervisor_comment = Column(Text())


class TaskIpr(Base):
    ipr_id = Column(
        Integer,
        ForeignKey('ipr.id', ondelete='CASCADE')
    )
    task_id = Column(
        Integer,
        ForeignKey('task.id', ondelete='CASCADE')
    )
