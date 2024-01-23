from datetime import date, datetime
from typing import Optional, List

from pydantic import BaseModel, validator

from app.schemas.educations import EducationsDB


class TaskDB(BaseModel):
    id: Optional[int]
    name: Optional[str]
    dateOfEnd: Optional[date]
    description: Optional[str]
    educations: Optional[List[EducationsDB]]
    commentOfMentor: Optional[str]
    status: str

    @validator('dateOfEnd', check_fields=False)
    def validate_date_format(cls, value):
        try:
            parsed_date = datetime.strptime(value, "%d.%m.%Y").date()
            return parsed_date
        except ValueError:
            raise ValueError('Отправлен некорректный запрос серверу. Необходимо проверить параметры запроса.')
