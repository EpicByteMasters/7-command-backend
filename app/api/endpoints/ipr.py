from http import HTTPStatus

from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from app.api.validators import (
    check_current_user_is_employees_supervisor,
    check_ipr_is_draft,
    check_ipr_is_in_progress,
    check_user_exists,
    check_user_is_ipr_employee,
    check_user_is_ipr_supervisor,
    check_user_is_supervisor,
    check_user_is_ipr_mentor_or_supervisor,
    check_ipr_is_in_progress,
)
from app.api.utils import (
    add_competencies,
    update_task_employee,
    update_tasks,
    demote_user_as_mentor
)
from app.core.db import get_async_session
from app.core.user import current_user
from app.crud import ipr_crud
from app.models import User
from app.schemas.new_ipr import (
    IprComplete,
    IPRDraftCreate,
    IPRDraftCreateOut,
    IPRDraftIn,
    IPRDraftOut,
    IPRDraftUpdate,
    IPREmployeeOut,
    IPRSupervisorOut,
    IprListOut,
    IprListSupervisorOut,
    IprUpdateEmployeeIn,
    IprUpdateSupervisorIn
)


router = APIRouter()


@router.post("/create",
             response_model=IPRDraftCreateOut,
             response_model_exclude_none=True,
             status_code=HTTPStatus.CREATED,
             dependencies=[Depends(current_user)],
             summary='Создать черновик руководителем',
             tags=['ИПР'])
async def create_new_ipr(draft_ipr: IPRDraftCreate,
                         session: AsyncSession = Depends(get_async_session),
                         user: User = Depends(current_user)):
    check_user_is_supervisor(user)
    employee_id = draft_ipr.employee_id
    await check_current_user_is_employees_supervisor(employee_id,
                                                     user,
                                                     session)
    await ipr_crud.check_user_does_not_have_draft_iprs(employee_id, session)
    ipr_draft = await ipr_crud.create_ipr_draft(draft_ipr, user.id, session)
    return ipr_draft


@router.get("/employees/my-iprs",
            response_model=list[IprListOut],
            response_model_exclude_none=True,
            status_code=HTTPStatus.OK,
            dependencies=[Depends(current_user)],
            tags=["ИПР"])
async def get_my_iprs(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    iprs = await ipr_crud.get_users_ipr(user, session)
    return iprs


@router.get("/{employee_id}/list-iprs",
            response_model=list[IprListSupervisorOut],
            response_model_exclude_none=True,
            status_code=HTTPStatus.OK,
            dependencies=[Depends(current_user)])
async def get_users_iprs(employee_id: int,
                         user: User = Depends(current_user),
                         session: AsyncSession = Depends(get_async_session)):
    employee = await check_user_exists(employee_id, session)
    await check_current_user_is_employees_supervisor(employee_id, user, session)
    iprs = await ipr_crud.get_users_ipr_by_supervisor(employee, session)
    return iprs


@router.patch("/{ipr_id}/save-draft",
              response_model=IPRDraftOut,
              response_model_exclude_none=True,
              summary='Сохранить черновик',
              tags=['ИПР'])
async def save_draft(ipr_id: int,
                     draft_data_in: IPRDraftIn,
                     user: User = Depends(current_user),
                     session: AsyncSession = Depends(get_async_session)):
    ipr = await ipr_crud.check_ipr_exists(ipr_id, session)
    check_user_is_ipr_supervisor(ipr, user)

    draft_data_in = draft_data_in.dict()
    mentor_id = draft_data_in.get("mentor_id", None)
    if mentor_id is not None:
        await check_user_exists(mentor_id, session)
    draft_data_in = await update_tasks(draft_data_in, ipr_id, session)
    draft_data_in = await add_competencies(draft_data_in, ipr_id, session)

    draft_data_in = IPRDraftUpdate.parse_obj(draft_data_in)
    ipr = await ipr_crud.update_ipr(draft_data_in, ipr, session)
    return ipr


@router.get("/test-list-iprs",
            response_model=list[IPRSupervisorOut])
async def get_all_iprs(session: AsyncSession = Depends(get_async_session)):
    """Отладочный эндпоинт"""
    iprs = await ipr_crud.get_multi(session)
    return iprs


@router.get('/{ipr_id}/supervisor',
            response_model=IPRSupervisorOut,
            response_model_exclude_none=True,
            tags=['ИПР'],
            dependencies=[Depends(current_user)])
async def get_ipr_by_supervisor(ipr_id: int,
                                user: User = Depends(current_user),
                                session: AsyncSession = Depends(get_async_session)):
    ipr = await ipr_crud.check_ipr_exists(ipr_id, session)
    check_user_is_ipr_supervisor(ipr, user)
    return ipr


@router.get('/{ipr_id}/employee',
            response_model=IPREmployeeOut,
            response_model_exclude_none=True,
            tags=['ИПР'],
            dependencies=[Depends(current_user)])
async def get_ipr_employee(ipr_id: int,
                           user: User = Depends(current_user),
                           session: AsyncSession = Depends(get_async_session)):
    ipr = await ipr_crud.check_ipr_exists(ipr_id, session)
    check_user_is_ipr_employee(ipr, user)
    return ipr


@router.patch("/{ipr_id}/edit-ipr",
              response_model=IPRSupervisorOut,
              response_model_exclude_none=True,
              dependencies=[Depends(current_user)],
              summary="Редактировать ИПР руководителем",
              tags=['ИПР'])
async def edit_ipr_by_supervisor(ipr_id: int,
                                 update_data_in: IprUpdateSupervisorIn,
                                 user: User = Depends(current_user),
                                 session: AsyncSession = Depends(get_async_session)):
    ipr = await ipr_crud.check_ipr_exists(ipr_id, session)
    check_user_is_ipr_supervisor(ipr, user)

    update_data_in = update_data_in.dict()
    new_mentor_id = update_data_in.get("mentor_id", None)
    old_mentor_id = ipr.mentor_id
    if new_mentor_id is None:
        new_mentor = None
    else:
        new_mentor = await check_user_exists(new_mentor_id, session)

    update_data_in = await update_tasks(update_data_in, ipr_id, session)
    update_data_in = await add_competencies(update_data_in, ipr_id, session)

    if new_mentor is not None:
        if not new_mentor.is_mentor:
            new_mentor.is_mentor = True
            session.add(user)
        await demote_user_as_mentor(ipr_id, old_mentor_id, session)

    update_data_in = IPRDraftUpdate.parse_obj(update_data_in)
    ipr = await ipr_crud.update_ipr(update_data_in, ipr, session)
    return ipr


@router.patch("/{ipr_id}/edit-ipr-employee",
              response_model=IPREmployeeOut,
              response_model_exclude_none=False,
              dependencies=[Depends(current_user)],
              summary="Редактировать ИПР сотрудником",
              tags=['ИПР'])
async def edit_ipr_by_employee(ipr_id: int,
                               update_data_in: IprUpdateEmployeeIn,
                               user: User = Depends(current_user),
                               session: AsyncSession = Depends(get_async_session)):
    ipr = await ipr_crud.check_ipr_exists(ipr_id, session)
    check_user_is_ipr_employee(ipr, user)
    update_data_dict = update_data_in.dict()
    tasks = update_data_dict.pop("tasks", None)
    await update_task_employee(tasks, ipr, session)
    return ipr


@router.patch("/{ipr_id}/start-ipr",
              response_model=IPRSupervisorOut,
              response_model_exclude_none=False,
              dependencies=[Depends(current_user)],
              status_code=HTTPStatus.CREATED,
              tags=['ИПР'])
async def start_ipr(ipr_id: int,
                    update_data_in: IprUpdateSupervisorIn,
                    user: User = Depends(current_user),
                    session: AsyncSession = Depends(get_async_session)):
    ipr = await ipr_crud.check_ipr_exists(ipr_id, session)
    check_user_is_ipr_supervisor(ipr, user)
    check_ipr_is_draft(ipr)
    await ipr_crud.check_user_does_not_have_active_iprs(ipr.employee_id, session)

    update_data_in = update_data_in.dict()
    new_mentor_id = update_data_in.get("mentor_id", None)
    old_mentor_id = ipr.mentor_id
    if new_mentor_id is None:
        new_mentor = None
    else:
        new_mentor = await check_user_exists(new_mentor_id, session)

    update_data_in = await update_tasks(update_data_in, ipr_id, session)
    update_data_in = await add_competencies(update_data_in, ipr_id, session)

    if new_mentor is not None and not new_mentor.is_mentor:
        new_mentor.is_mentor = True
        session.add(new_mentor)
        await demote_user_as_mentor(ipr_id, old_mentor_id, session)
    else:
        old_mentor = await session.get(User, old_mentor_id)
        if not old_mentor.is_mentor:
            old_mentor.is_mentor = True
            session.add(old_mentor)

    update_data_in = IPRDraftUpdate.parse_obj(update_data_in)

    ipr = await ipr_crud.to_work(ipr, session)
    ipr = await ipr_crud.update_ipr(update_data_in, ipr, session)
    return ipr


@router.patch("/{ipr_id}/cancel",
              response_model=IPRSupervisorOut,
              response_model_exclude_none=True,
              dependencies=[Depends(current_user)],
              status_code=HTTPStatus.OK,
              tags=["ИПР"])
async def cancel_ipr(ipr_id=int,
                     user: User = Depends(current_user),
                     session: AsyncSession = Depends(get_async_session)):
    ipr = await ipr_crud.get_ipr_by_id(ipr_id, session)
    check_user_is_ipr_mentor_or_supervisor(ipr, user)
    check_ipr_is_in_progress(ipr)
    ipr = await ipr_crud.to_cancel(ipr, session)
    return ipr


@router.patch("/{ipr_id}/delete",
              dependencies=[Depends(current_user)],
              tags=["ИПР"])
async def remove_ipr(
    ipr_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    ipr = await ipr_crud.check_ipr_exists(ipr_id, session)
    check_user_is_ipr_supervisor(ipr, user)
    await ipr_crud.remove_ipr(ipr_id, session)
    return Response(status_code=HTTPStatus.NO_CONTENT)


@router.patch('/{ipr_id}/complete',
              response_model=IPRSupervisorOut,
              response_model_exclude_none=True,
              dependencies=[Depends(current_user)],
              tags=['ИПР'])
async def ipr_complete(ipr_id: int,
                       ipr_patch: IprComplete,
                       user: User = Depends(current_user),
                       session: AsyncSession = Depends(get_async_session)):
    ipr = ipr_crud.get_ipr_by_id(ipr_id, session)
    check_user_is_ipr_mentor_or_supervisor(ipr, user)
    check_ipr_is_in_progress(ipr)
    ipr = await ipr_crud.to_complete(ipr_patch, ipr_id, session)
    return ipr
