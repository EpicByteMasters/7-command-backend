from http import HTTPStatus

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from app.api.utils import add_competencies, create_tasks, get_foreign_keys_by_names
from app.core.db import get_async_session
from app.core.user import current_user
from app.crud import ipr_crud
from app.models.user import User
from app.schemas.ipr import (
    IprDraftCreate,
    IprDraftUpdate,
    IprDraftUpdateInput,
    IprDraftReturn,
)


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
