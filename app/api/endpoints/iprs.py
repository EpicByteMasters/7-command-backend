from http import HTTPStatus
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud import ipr_crud, user_crud, task_crud
from app.core.user import current_user
from app.models.user import User
from app.schemas.ipr import IprsOut

router = APIRouter()


@router.get(
    "/",
    response_model=list[IprsOut],
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)]
)
async def get_iprs(
    take: int = -1,
    skip: int = 0,
    statusipr: str = None,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Получить список ИПР руководителя по сотрудникам,
    используя ограничение количества результатов и смещение
    с фильтрацией по статусу ИПР
    """

    users = await user_crud.get_users_by_boss(user, session)
    resalt = []
    total_count_employee = 0
    total_count_iprs = 0
    if take < 0:
        use_take = False
        take = 2
    else:
        use_take = True

    for usr in users:
        ipr = await ipr_crud.get_last_users_ipr(usr, session)
        if ipr is not None:
            tasks = await task_crud.get_multi_task_by_iprid(ipr.id, session)
            task_count = 0
            task_completed = 0
            for r_task in tasks:
                task_count += 1
                if r_task.task_status_id == "COMPLETED":
                    task_completed += 1
            if ipr.close_date:
                r_date = ipr.close_date.strftime("%Y-%m-%d")
            else:
                r_date = None
            if (statusipr is None) or (statusipr == ipr.ipr_status_id):
                total_count_iprs += 1
                total_count_employee += 1
                if not use_take:
                    take += 1
                if skip < total_count_employee <= (take + skip):
                    resalt.append(
                        {
                            "id": usr.id,
                            "firstName": usr.first_name,
                            "lastName": usr.surname,
                            "middleName": usr.patronymic,
                            "positionId": usr.position_id,
                            "imageUrl": usr.image_url,
                            "iprId": ipr.id,
                            "goalId": ipr.goal_id,
                            "dateOfEnd": r_date,
                            "taskCompleted": task_completed,
                            "taskCount": task_count,
                            "statusId": ipr.ipr_status_id,
                        }
                    )

        else:
            if (statusipr is None) or (statusipr == "NO_IPR"):
                total_count_employee += 1
                if not use_take:
                    take += 1
                if skip < total_count_employee <= (take + skip):
                    resalt.append(
                        {
                            "id": usr.id,
                            "firstName": usr.first_name,
                            "lastName": usr.surname,
                            "middleName": usr.patronymic,
                            "position_id": usr.position_id,
                            "imageUrl": usr.image_url,
                            "statusId": "NO_IPR",
                        }
                    )

    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={
            "employees": resalt,
            "totalСountIpsr": total_count_iprs,
            "totalCountEmployee": total_count_employee,
        },
    )
