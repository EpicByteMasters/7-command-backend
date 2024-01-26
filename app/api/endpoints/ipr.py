from http import HTTPStatus

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from fastapi.responses import Response

from app.api.utils import add_competencies, create_or_update_tasks
from app.core.db import get_async_session
from app.core.user import current_user
from app.crud import ipr_crud, task_crud
from app.models.user import User
from app.schemas.ipr import (
    IprDraftCreate,
    IprDraftUpdate,
    IprDraftUpdateInput,
    IprDraftReturn,
    IprUpdate
)


router = APIRouter()


@router.patch("/{ipr_id}/save-draft",
              dependencies=[Depends(current_user)],
              status_code=HTTPStatus.CREATED)
async def save_draft(ipr_id: int,
                     draft_data_in: IprDraftUpdateInput,
                     session: AsyncSession = Depends(get_async_session),):
    ipr = await ipr_crud.get_ipr_by_id(ipr_id, session)

    draft_data_in = draft_data_in.dict()
    draft_data_in = await create_or_update_tasks(draft_data_in, ipr_id, session)
    draft_data_in = await add_competencies(draft_data_in, ipr_id, session)

    draft_data_in = IprDraftUpdate.parse_obj(draft_data_in)
    ipr = await ipr_crud.update(draft_data_in, ipr, session)
    return ipr


@router.patch("/{ipr_id}/edit-ipr",
              dependencies=[Depends(current_user)],
              status_code=HTTPStatus.CREATED)
async def edit_ipr(ipr_id: int,
                   update_data_in: IprUpdate,
                   session: AsyncSession = Depends(get_async_session)):
    ipr = await ipr_crud.get_ipr_by_id(ipr_id, session)

    update_data_in = update_data_in.dict()
    update_data_in = await create_or_update_tasks(update_data_in, ipr_id, session)
    update_data_in = await add_competencies(update_data_in, ipr_id, session)

    update_data_in = IprDraftUpdate.parse_obj(update_data_in)
    ipr = await ipr_crud.update(update_data_in, ipr, session)
    return ipr


@router.delete("/{ipr_id}/edit-ipr/task/{task_id}/remove",
               dependencies=[Depends(current_user)],
               status_code=HTTPStatus.CREATED)
async def remove_task_from_ipr(task_id: int,
                               session: AsyncSession = Depends(get_async_session)):
    task = await task_crud.get(task_id, session)
    await task_crud.remove(task, session)
    return {}


@router.post("/create",
             response_model=IprDraftReturn,
             status_code=HTTPStatus.CREATED,
             dependencies=[Depends(current_user)],)
async def create_new_ipr(draft_ipr: IprDraftCreate,
                         session: AsyncSession = Depends(get_async_session),
                         user: User = Depends(current_user)):
    draft_ipr.supervisor_id = user.id
    draft_ipr.ipr_status_id = 1
    ipr_draft = await ipr_crud.create(draft_ipr, session)
    return ipr_draft


@router.delete("/{ipr_id}",
               dependencies=[Depends(current_user)])
async def remove_ipr(ipr_id: int,
                     user: User = Depends(current_user),
                     session: AsyncSession = Depends(get_async_session)):
    await ipr_crud.remove_ipr(user, ipr_id, session)
    return Response(status_code=HTTPStatus.NO_CONTENT)
