from datetime import date, datetime
from typing import Optional, List

from pydantic import BaseModel, validator

from app.schemas.task import TaskDB


class IPRDraftSave(BaseModel):
    goal: Optional[str]
    specialization: Optional[str]
    competence: List[str]
    createdAt: Optional[date]
    dateOfEnd: Optional[date]
    mentorId: Optional[str]
    description: Optional[str]
    comment: Optional[str]
    tasks: Optional[TaskDB]
    status: str

    @validator('dateOfEnd', 'createdAt', check_fields=False)
    def validate_date_format(cls, value):
        try:
            parsed_date = datetime.strptime(value, "%d.%m.%Y").date()
            return parsed_date
        except ValueError:
            raise ValueError('Отправлен некорректный запрос серверу. Необходимо проверить параметры запроса.')

    @validator('createdAt', 'dateOfEnd', check_fields=False)
    def validate_start_end_dates(cls, values):
        if 'createdAt' in values and 'dateOfEnd' in values:
            if values['createdAt'] >= values['dateOfEnd']:
                raise ValueError("Дата конца должна быть после даты создания")

        return values
