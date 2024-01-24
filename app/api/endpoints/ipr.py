from http import HTTPStatus

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from app.core.db import get_async_session
from app.core.user import current_user
from app.crud import (
    competency_crud,
    competency_ipr_crud,
    education_crud,
    education_task_crud,
    goal_crud,
    ipr_crud,
    specialty_crud,
    task_crud,
)
from app.models.user import User
from app.schemas.ipr import (
    IprDraftCreate,
    IprDraftUpdate,
    IprDraftUpdateInput,
    IprDraftReturn,
    CompetencyIprCreate,
)
from app.schemas.task import TaskCreate, EduTaskCreate


router = APIRouter()


@router.put(
    "/{ipr_id}/save-draft",
    dependencies=[Depends(current_user)],
    status_code=HTTPStatus.CREATED,
)
async def save_draft(
    ipr_id: int,
    new_draft_ipr: IprDraftUpdateInput,
    session: AsyncSession = Depends(get_async_session),
):
    ipr = await ipr_crud.get_ipr_by_id(ipr_id, session)

    new_draft_dict = new_draft_ipr.dict()
    new_draft_dict = await create_tasks(new_draft_dict, ipr_id, session)
    new_draft_dict = await add_competencies(new_draft_dict, ipr_id, session)
    new_draft_dict = await get_foreign_keys_by_names(new_draft_dict, session)

    new_draft_ipr = IprDraftUpdate.parse_obj(new_draft_dict)
    ipr = await ipr_crud.update(new_draft_ipr, ipr, session)
    return {}


@router.post(
    "/create",
    response_model=IprDraftReturn,
    status_code=HTTPStatus.CREATED,
    dependencies=[Depends(current_user)],
)
async def create_new_ipr(
    draft_ipr: IprDraftCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    draft_ipr.supervisor_id = user.id
    draft_ipr.ipr_status_id = 1
    ipr_draft = await ipr_crud.create(draft_ipr, session)
    return ipr_draft


@router.delete("/{ipr_id}", dependencies=[Depends(current_user)])
async def remove_ipr(ipr_id: int, session: AsyncSession = Depends(get_async_session)):
    ipr = await ipr_crud.check_ipr_exists(ipr_id, session)
    await ipr_crud.remove(ipr, session)
    return {}


async def add_competencies(
    new_draft_dict: dict, ipr_id: int, session: AsyncSession
) -> dict:
    competencies = new_draft_dict.pop("competence")
    if competencies is None:
        return new_draft_dict
    for comp in competencies:
        comp_id = await competency_crud.get_id_by_name(comp, session)
        connection = {"competency_id": comp_id, "ipr_id": ipr_id}
        schema = CompetencyIprCreate.parse_obj(connection)
        await competency_ipr_crud.create(schema, session)
    return new_draft_dict


async def create_tasks(new_draft_dict: dict, ipr_id, session) -> dict:
    tasks = new_draft_dict.pop("tasks")
    if tasks is None:
        return new_draft_dict
    for task in tasks:
        educations = task.pop("educations")
        task["ipr_id"] = ipr_id
        new_task = TaskCreate.parse_obj(task)
        task = await task_crud.create(new_task, session)
        task_id = task.id
        if educations is not None:
            for education in educations:
                education_id = await education_crud.get_id_by_name(
                    education["name"], session
                )
                education_task = {"task_id": task_id, "education_id": education_id}
                eduSchema = EduTaskCreate.parse_obj(education_task)
                await education_task_crud.create(eduSchema, session)
    return new_draft_dict


async def get_foreign_keys_by_names(new_draft_dict: dict, session) -> dict:
    goal = new_draft_dict["goal"]
    if goal is not None:
        goal_id = await goal_crud.get_id_by_name(goal, session)
        new_draft_dict["goal_id"] = goal_id
    specialty = new_draft_dict["specialty"]
    if specialty is not None:
        specialty_id = await specialty_crud.get_id_by_name(specialty, session)
        new_draft_dict["specialty_id"] = specialty_id
    return new_draft_dict
