from datetime import date

from app.schemas.base import AllOptional, Base


class NotificationGet(Base, metaclass=AllOptional):
    title: str
    brief_text: str
    button_text: str
    date: date
    url: str


class NotificationAddDB(Base):
    title: str
    brief_text: str
    button_text: str
    date: date
    url: str
    user_id: int


class NotificationAddDB(Base):
    title: str
    brief_text: str
    button_text: str
    date: date
    url: str
    user_id: int
