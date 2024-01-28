from pydantic import BaseModel

from .utils import to_camel


class DocBase(BaseModel):
    id: str
    name: str

    class Config:
        orm_mode = True
        alias_generator = to_camel
        allow_population_by_field_name = True


class EducationDoc(DocBase):
    id: int
    specialty: str
    url_link: str


class SpecialtyDoc(DocBase):
    pass


class TaskStatusDoc(DocBase):
    pass


class CompetencyDoc(DocBase):
    skill_type: str


class GoalDoc(DocBase):
    pass


class IprStatusDoc(DocBase):
    pass