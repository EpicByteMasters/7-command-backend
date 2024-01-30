from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from app.core.db import get_async_session
from app.crud import (
    competency_crud,
    education_crud,
    goal_crud,
    position_crud,
    specialty_crud,
    status_crud,
    task_status_crud,
)
from app.schemas.secondary import (
    CompetencyDoc,
    EducationDoc,
    GoalDoc,
    IprStatusDoc,
    PositionDoc,
    SpecialtyDoc,
    TaskStatusDoc,
)


router = APIRouter()


@router.get(
    "/ipr_status", response_model=list[IprStatusDoc], response_model_exclude_none=True
)
async def list_ipr_statuses(session: AsyncSession = Depends(get_async_session)):
    statuses = await status_crud.get_multi(session)
    return statuses


@router.get("/ipr_goal", response_model=list[GoalDoc], response_model_exclude_none=True)
async def list_ipr_goals(session: AsyncSession = Depends(get_async_session)):
    goals = await goal_crud.get_multi(session)
    return goals


@router.get(
    "/ipr_competency",
    response_model=list[CompetencyDoc],
    response_model_exclude_none=True,
)
async def list_ipr_competencies(session: AsyncSession = Depends(get_async_session)):
    competencies = await competency_crud.get_multi(session)
    return competencies


@router.get(
    "/task_status", response_model=list[TaskStatusDoc], response_model_exclude_none=True
)
async def list_task_statuses(session: AsyncSession = Depends(get_async_session)):
    task_statuses = await task_status_crud.get_multi(session)
    return task_statuses


@router.get(
    "/specialty", response_model=list[SpecialtyDoc], response_model_exclude_none=True
)
async def list_task_statuses(session: AsyncSession = Depends(get_async_session)):
    specialties = await specialty_crud.get_multi(session)
    return specialties


@router.get(
    "/education", response_model=list[EducationDoc], response_model_exclude_none=True
)
async def list_educations(session: AsyncSession = Depends(get_async_session)):
    educations = await education_crud.get_multi(session)
    return educations


@router.get(
    "/position", response_model=list[PositionDoc], response_model_exclude_none=True
)
async def list_positions(session: AsyncSession = Depends(get_async_session)):
    positions = await position_crud.get_multi(session)
    return positions
