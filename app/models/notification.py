from sqlalchemy import Column, Date, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.core.db import Base


class Notification(Base):
    title = Column(Text(256), nullable=True)
    brief_text = Column(Text(256), nullable=True)
    button_text = Column(Text(64), nullable=True)
    date = Column(Date, nullable=True)
    ipr_id = Column(Integer, ForeignKey("ipr.id"), default=0)
    ipr = relationship("Ipr", back_populates="notifications")
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="notifications")
    task_id = Column(Integer, ForeignKey("task.id"), default=0)
    task = relationship("Task", back_populates="notifications")
