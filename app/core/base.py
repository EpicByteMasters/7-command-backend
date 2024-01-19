"""Импорты класса Base и всех моделей для Alembic."""
from app.core.db import Base  # noqa
from app.models import (  # noqa
    Competency,
    CompetencyLearning,
    CompetencyIpr,
    CompetencySpecialty,
    Education,
    EducationTask,
    Goal,
    Grade,
    Ipr,
    Position,
    Specialty,
    SpecialtyEducation,
    Status,
    Task,
    TaskFile,
    TaskIpr,
    TaskStatus,
    User,
)
