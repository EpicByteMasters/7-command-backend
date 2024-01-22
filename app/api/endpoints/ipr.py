from http import HTTPStatus

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException

from app.core.db import get_async_session
from app.schemas.ipr import IPRDraftCreate, IPRDraftSave
from app.crud.ipr import (
    create_ipr,
    check_ipr_exists,
    get_status_id_by_name,
    get_status_by_id,
    delete_ipr,
)

router = APIRouter()


@router.put("/mentor/iprs/ipr/:id/save-draft", response_model=IPRDraftSave)
async def save_draft(
    session: AsyncSession = Depends(get_async_session),
    # user: User = Depends(get_current_user())
):
    pass


@router.post("/mentor/iprs/ipr/create", status_code=HTTPStatus.CREATED)
async def create_new_ipr(
    draft_ipr: IPRDraftCreate, session: AsyncSession = Depends(get_async_session)
):

    status_id = await get_status_id_by_name("DRAFT", session)
    if status_id is None:
        raise HTTPException(status_code=422, detail="Статус DRAFT не найден в БД")
    draft_ipr.ipr_status_id = status_id
    draft_ipr.supervisor_id = 30  # Not null в модели

    new_ipr = await create_ipr(draft_ipr, session)
    status_name = await get_status_by_id(new_ipr.ipr_status_id, session)
    return {"id": new_ipr.id, "status": status_name}


@router.delete("/mentor/iprs/ipr/{ipr_id}")
async def remove_ipr(
    ipr_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    ipr = await check_ipr_exists(ipr_id, session)
    await delete_ipr(ipr, session)
    return {}
