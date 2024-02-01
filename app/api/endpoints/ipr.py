from http import HTTPStatus

from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from app.api.validators import (
    check_ipr_is_draft,
    check_user_is_ipr_supervisor,
    check_user_is_supervisor,
    check_current_user_is_employees_supervisor,
    check_user_is_ipr_employee_or_supervisor,
    check_user_is_ipr_mentor_or_supervisor,
    check_ipr_is_in_progress
)
from app.api.utils import (add_competencies, update_tasks)
from app.core.db import get_async_session
from app.core.user import current_user
from app.crud import ipr_crud
from app.models.user import User
from app.schemas.ipr import (
    IprListRead,
    IprDraftDB,
    IprDraftCreate,
    IprDraftUpdate,
    IprDraftUpdateInput,
    IprUpdate,
    IprComplete
)


router = APIRouter()


@router.post("/create",
             response_model=IprDraftDB,
             response_model_exclude_none=True,
             status_code=HTTPStatus.CREATED,
             dependencies=[Depends(current_user)],
             tags=['ИПР'])
async def create_new_ipr(draft_ipr: IprDraftCreate,
                         session: AsyncSession = Depends(get_async_session),
                         user: User = Depends(current_user)):
    check_user_is_supervisor(user)
    employee_id = draft_ipr.employee_id
    await check_current_user_is_employees_supervisor(employee_id,
                                                     user,
                                                     session)
    await ipr_crud.check_user_does_not_have_active_iprs(employee_id, session)
    ipr_draft = await ipr_crud.create_ipr_draft(draft_ipr, user.id, session)
    return ipr_draft


@router.get("/employees/my_iprs",
            response_model=list[IprListRead],
            response_model_exclude_none=True,
            status_code=HTTPStatus.OK,
            dependencies=[Depends(current_user)],
            tags=['ИПР'])
async def get_my_iprs(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    iprs = await ipr_crud.get_users_ipr(user, session)
    return iprs


@router.patch("/{ipr_id}/save-draft",
              response_model=IprDraftDB,
              response_model_exclude_none=True,
              tags=['ИПР'])
async def save_draft(ipr_id: int,
                     draft_data_in: IprDraftUpdateInput,
                     user: User = Depends(current_user),
                     session: AsyncSession = Depends(get_async_session)):
    ipr = await ipr_crud.check_ipr_exists(ipr_id, session)
    check_user_is_ipr_supervisor(ipr, user)

    draft_data_in = draft_data_in.dict()
    draft_data_in = await update_tasks(draft_data_in, ipr_id, session)
    draft_data_in = await add_competencies(draft_data_in, ipr_id, session)

    draft_data_in = IprDraftUpdate.parse_obj(draft_data_in)
    ipr = await ipr_crud.update(draft_data_in, ipr, session)
    return ipr


@router.get("/test-list-iprs",
            response_model=list[IprDraftDB])
async def get_all_iprs(session: AsyncSession = Depends(get_async_session)):
    """Отладочный эндпоинт"""
    iprs = await ipr_crud.get_multi(session)
    return iprs


@router.get('/{ipr_id}',
            response_model=IprDraftDB,
            response_model_exclude_none=True,
            tags=['ИПР'],
            dependencies=[Depends(current_user)])
async def get_ipr(ipr_id: int,
                  user: User = Depends(current_user),
                  session: AsyncSession = Depends(get_async_session)):
    ipr = await ipr_crud.check_ipr_exists(ipr_id, session)
    check_user_is_ipr_employee_or_supervisor(ipr, user)
    return ipr


@router.patch("/{ipr_id}/edit-ipr",
              response_model=IprDraftDB,
              response_model_exclude_none=True,
              dependencies=[Depends(current_user)],
              status_code=HTTPStatus.CREATED,
              tags=['ИПР'])
async def edit_ipr(ipr_id: int,
                   update_data_in: IprUpdate,
                   user: User = Depends(current_user),
                   session: AsyncSession = Depends(get_async_session)):
    ipr = await ipr_crud.check_ipr_exists(ipr_id, session)
    check_user_is_ipr_supervisor(ipr, user)

    update_data_in = update_data_in.dict()
    update_data_in = await update_tasks(update_data_in, ipr_id, session)
    update_data_in = await add_competencies(update_data_in, ipr_id, session)

    update_data_in = IprDraftUpdate.parse_obj(update_data_in)
    ipr = await ipr_crud.update(update_data_in, ipr, session)
    return ipr


@router.patch("/{ipr_id}/start-ipr",
              response_model=IprDraftDB,
              response_model_exclude_none=True,
              dependencies=[Depends(current_user)],
              status_code=HTTPStatus.CREATED,
              tags=['ИПР'])
async def start_ipr(ipr_id: int,
                    update_data_in: IprUpdate,
                    user: User = Depends(current_user),
                    session: AsyncSession = Depends(get_async_session)):
    ipr = await ipr_crud.check_ipr_exists(ipr_id, session)
    check_ipr_is_draft(ipr)
    check_user_is_ipr_supervisor(ipr, user)

    update_data_in = update_data_in.dict()
    update_data_in = await update_tasks(update_data_in, ipr_id, session)
    update_data_in = await add_competencies(update_data_in, ipr_id, session)

    update_data_in = IprDraftUpdate.parse_obj(update_data_in)
    print(ipr.goal)
    ipr = await ipr_crud.to_work(ipr, session)
    print(ipr.goal)
    ipr = await ipr_crud.update(update_data_in, ipr, session)
    return ipr


@router.post("/{ipr_id}",
             dependencies=[Depends(current_user)],
             tags=['ИПР'])
async def remove_ipr(ipr_id: int,
                     user: User = Depends(current_user),
                     session: AsyncSession = Depends(get_async_session)):
    ipr = await ipr_crud.check_ipr_exists(ipr_id, session)
    check_user_is_ipr_supervisor(ipr, user)
    await ipr_crud.remove_ipr(user, ipr_id, session)
    return Response(status_code=HTTPStatus.NO_CONTENT)


@router.patch('/{ipr_id}/complete',
              dependencies=[Depends(current_user)],
              tags=['ИПР'])
async def ipr_complete(ipr_id: int,
                       ipr_patch: IprComplete,
                       user: User = Depends(current_user),
                       session: AsyncSession = Depends(get_async_session)):
    ipr = ipr_crud.get_ipr_by_id(ipr_id, session)
    check_user_is_ipr_mentor_or_supervisor(ipr, user)
    check_ipr_is_in_progress(ipr)
    await ipr_crud.to_complete(ipr_patch, ipr_id, session)
    return HTTPStatus.OK
