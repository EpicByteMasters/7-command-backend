from http import HTTPStatus

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.ipr import ipr_crud
from app.models.user import User
from app.schemas.ipr import IPRDraftCreate, IPRDraftSave, IPRDraftReturn


router = APIRouter()


@router.put("/mentor/iprs/ipr/<draft_id>/save-draft",
            response_model=IPRDraftSave,
            dependencies=[Depends(current_user)],
            status_code=HTTPStatus.CREATED)
async def save_draft(draft_id: int,
                     draft_ipr: IPRDraftSave,
                     session: AsyncSession = Depends(get_async_session),
                     user: User = Depends(current_user),):
    return await ipr_crud.update(session, draft_id, draft_ipr, user)


@router.post("/mentor/iprs/ipr/create",
             response_model=IPRDraftReturn,
             status_code=HTTPStatus.CREATED,
             dependencies=[Depends(current_user)])
async def create_new_ipr(draft_ipr: IPRDraftCreate,
                         session: AsyncSession = Depends(get_async_session),
                         user: User = Depends(current_user)):
    return await ipr_crud.create_ipr_draft(draft_ipr, session)


@router.delete("/mentor/iprs/ipr/{ipr_id}",
               dependencies=[Depends(current_user)])
async def remove_ipr(ipr_id: int,
                     user: User = Depends(current_user),
                     session: AsyncSession = Depends(get_async_session)):
    # ipr = await ipr_crud.check_ipr_exists(ipr_id, session)
    await ipr_crud.delete_ipr(ipr_id, session, user)
    return {}
