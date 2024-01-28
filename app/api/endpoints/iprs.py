from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud import ipr_crud, user_crud, task_crud
from app.core.user import current_user
from app.models.user import User

router = APIRouter()


@router.get(
    "/",
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)]
)
async def get_iprs(take: int,
                   skip: int,
                   statusipr: str = None,
                   user: User = Depends(current_user),
                   session: AsyncSession = Depends(get_async_session),
                   ):
    """
    Получить список ИПР руководителя,
    используя ограничение количества результатов и смещение
    с фильтрацией по статусу ИПР
    """

    iprs = await ipr_crud.get_supervisors_ipr(take, skip, statusipr, user, session)
    resalt = []
    totalcount = 0
    for ipr in iprs:
        tasks = await task_crud.get_multi_task_by_iprid(ipr.id, session)
        task_count = 0
        task_completed = 0
        for r_task in tasks:
            task_count += 1
            if r_task.task_status == "COMPLETED":
                task_completed += 1
        progress = str(task_completed) + '/' + str(task_count)
        r_user = await user_crud.get(ipr.employee_id, session)
        resalt.append({"user": r_user, "ipr": ipr, "progress": progress})
        totalcount += 1

    return {"employees": resalt, "totalcount": totalcount}
