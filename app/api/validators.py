from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import task_crud, user_crud
from app.models import Ipr, User


def check_user_is_ipr_employee(ipr: Ipr, user: User) -> None:
    if ipr.employee_id != user.id:
        raise HTTPException(
            HTTPStatus.FORBIDDEN,
            detail="У вас нет прав модифицировать/удалять данный ИПР",
        )


def check_user_is_ipr_mentor_or_supervisor(ipr: Ipr, user: User) -> None:
    if ipr.supervisor_id != user.id and ipr.mentor_id != user.id:
        raise HTTPException(
            HTTPStatus.FORBIDDEN,
            detail="У вас нет прав модифицировать/удалять данный ИПР",
        )


def check_ipr_is_in_progress(ipr) -> None:
    if ipr.ipr_status_id != "IN_PROGRESS":
        raise HTTPException(
            HTTPStatus.FORBIDDEN,
            detail="Данный ИПР нельзя отменить",
        )


def check_user_is_ipr_supervisor(ipr: Ipr, user: User) -> None:
    if ipr.supervisor_id != user.id:
        raise HTTPException(
            HTTPStatus.FORBIDDEN,
            detail="У вас нет прав модифицировать/удалять данный черновик ИПР",
        )


def check_ipr_is_in_progress(ipr) -> None:
    if ipr.ipr_status_id != "IN_PROGRESS":
        raise HTTPException(
            HTTPStatus.FORBIDDEN,
            detail="Данный ИПР нельзя завершить или отменить",
        )


def check_user_is_supervisor(user: User) -> None:
    if not user.is_supervisor:
        raise HTTPException(
            HTTPStatus.FORBIDDEN,
            detail="У вас нет прав модифицировать/удалять данный черновик ИПР",
        )


async def check_current_user_is_employees_supervisor(employee_id: int,
                                                     user: User,
                                                     session: AsyncSession):
    employee = await user_crud.get(employee_id, session)
    if employee.supervisor_id != user.id:
        raise HTTPException(
            HTTPStatus.FORBIDDEN,
            detail="Вы не являетесь руководителем данного сотрудника"
        )


def check_ipr_is_draft(ipr: Ipr) -> None:
    if ipr.ipr_status_id != "DRAFT":
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Данный ИПР уже был запущен в работу"
        )


async def check_current_user_is_employees_supervisor(
    employee_id: int, user: User, session: AsyncSession
):
    employee = await user_crud.get(employee_id, session)
    if employee.supervisor_id != user.id:
        raise HTTPException(
            HTTPStatus.FORBIDDEN,
            detail="Вы не являетесь руководителем данного сотрудника",
        )


async def check_user_exists(user_id, session: AsyncSession):
    user = await user_crud.check_user_exists(user_id, session)
    if user is None:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                            detail="В поле введен несуществующий пользователь")
    return user


async def check_task_exists_in_ipr(task_id, ipr_id, session):
    db_task = await task_crud.check_task_in_ipr(task_id,
                                                ipr_id,
                                                session)
    if db_task is None:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                            detail="Задачи с таким id не найдена в данном ИПР")
    return db_task
