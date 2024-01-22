from datetime import date, datetime
from typing import Optional, List

from pydantic import BaseModel, validator, Field

from app.schemas.task import TaskDB


class IPRDraftCreate(BaseModel):
    emplyee_id: int = Field(alias="employeeId")
    supervisor_id: Optional[int]
    goal_id: Optional[int]
    specialty_id: Optional[int]
    create_date: Optional[date]
    close_date: Optional[date]
    mentor_id: Optional[int]
    description: Optional[str]
    comment: Optional[str]
    ipr_status_id: Optional[int]
    ipr_grade_id: Optional[int]
    supervisor_comment: Optional[str]

    class Config:
        allow_population_by_field_name = True


class IPRDraftSave(BaseModel):
    goal: Optional[str]
    specialization: Optional[str]
    competency: List[str]
    createdAt: Optional[date]
    dateOfEnd: Optional[date]
    mentorId: Optional[str]
    description: Optional[str]
    comment: Optional[str]
    tasks: Optional[TaskDB]
    status: str

    @validator("dateOfEnd", "createdAt", check_fields=False)
    def validate_date_format(cls, value):
        try:
            parsed_date = datetime.strptime(value, "%d.%m.%Y").date()
            return parsed_date
        except ValueError:
            raise ValueError(
                "Отправлен некорректный запрос серверу. Необходимо проверить параметры запроса."
            )

    @validator("createdAt", "dateOfEnd", check_fields=False)
    def validate_start_end_dates(cls, values):
        if "createdAt" in values and "dateOfEnd" in values:
            if values["createdAt"] >= values["dateOfEnd"]:
                raise ValueError("Дата конца должна быть после даты создания")

        return values
