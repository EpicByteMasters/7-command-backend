from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.user import user_crud
from app.models import Ipr, User


def check_ipr_user(ipr: Ipr,
                   user: User) -> None:
    if ipr.employee_id != user.id or ipr.supervisor_id != user.id:
        raise HTTPException(
            HTTPStatus.FORBIDDEN,
            detail="У вас нет прав модифицировать/удалять данный ИПР",
        )


def check_user_is_ipr_supervisor():
    pass


def check_user_is_ipr_employee_or_supervisor():
    pass


def check_user_is_ipr_mentor_or_supervisor(ipr: Ipr, user: User) -> None:
    if ipr.supervisor_id != user.id or ipr.mentor_id != user.id:
        raise HTTPException(HTTPStatus.FORBIDDEN,
                            detail="У вас нет прав модифицировать/удалять данный ИПР")


def check_user_is_supervisor_in_ipr(ipr: Ipr,
                                    user: User) -> None:
    if ipr.supervisor_id != user.id:
        raise HTTPException(
            HTTPStatus.FORBIDDEN,
            detail="У вас нет прав модифицировать/удалять данный черновик ИПР",
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
