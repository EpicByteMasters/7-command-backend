from sqlalchemy import Column, Date, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.core.db import Base


class Notification(Base):
    title = Column(Text(256), nullable=True)
    briefText = Column(Text(256), nullable=True)
    date = Column(Date, nullable=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="notifications")
