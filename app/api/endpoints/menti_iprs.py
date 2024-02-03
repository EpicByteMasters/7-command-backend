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
    dependencies=[Depends(current_user)],
)
async def get_iprs(
    take: int = -1,
    skip: int = 0,
    statusipr: str = None,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Получить список ИПР ментора,
    используя ограничение количества результатов и смещение
    с фильтрацией по статусу ИПР
    """

    iprs = await ipr_crud.get_mentors_iprs(take, skip, statusipr, user, session)
    resalt = []
    total_count = 0
    for ipr in iprs:
        tasks = await task_crud.get_multi_task_by_iprid(ipr.id, session)
        task_count = 0
        task_completed = 0
        for r_task in tasks:
            task_count += 1
            if r_task.task_status_id == "COMPLETED":
                task_completed += 1
        r_user = await user_crud.get(ipr.employee_id, session)
        if ipr.close_date:
            r_date = ipr.close_date.strftime("%d-%m-%Y")
        else:
            r_date = None
        resalt.append(
            {
                "id": r_user.id,
                "firstName": r_user.first_name,
                "lastName": r_user.surname,
                "middleName": r_user.patronymic,
                "positionId": r_user.position_id,
                "imageUrl": r_user.image_url,
                "iprId": ipr.id,
                "goalId": ipr.goal_id,
                "dateOfEnd": r_date,
                "taskCompleted": task_completed,
                "taskCount": task_count,
                "statusId": ipr.ipr_status_id,
            }
        )
        total_count += 1

    return JSONResponse(
        status_code=200, content={"employees": resalt, "totalCount": total_count}
    )
