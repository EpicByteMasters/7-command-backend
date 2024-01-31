from datetime import date

from pydantic import BaseModel


class NotificationGet(BaseModel):
    title: str
    briefText: str
    date: date
    url: str


class NotificationAddDB(BaseModel):
    title: str
    briefText: str
    date: date
    url: str
    user_id: int


class NotificationAddDB(BaseModel):
    title: str
    briefText: str
    date: date
    url: str
    user_id: int
