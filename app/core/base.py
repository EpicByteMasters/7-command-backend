"""Импорты класса Base и всех моделей для Alembic."""
from app.core.db import Base  # noqa
from app.models import (  # noqa
    Competency,
    CompetencyEducation,
    CompetencyIpr,
    CompetencySpecialty,
    Education,
    EducationTask,
    Goal,
    Ipr,
    Position,
    Specialty,
    SpecialtyEducation,
    Status,
    Task,
    TaskFile,
    TaskStatus,
    User,
)
