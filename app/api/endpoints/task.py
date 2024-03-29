from datetime import date
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user
from app.crud import ipr_crud, notification_crud, task_crud
from app.models import Notification
from app.models.user import User

router = APIRouter()


@router.patch(
    "/{id}/complete",
    dependencies=[Depends(current_user)],
)
async def patch_task_complete(
    id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Поменять статус задачи IN_PROGRESS -> AWAITING_REVIEW"""
    task = await task_crud.get(id, session)
    if task.task_status_id != "IN_PROGRESS":
        exeption_delail = (
            "Задача уже находится на проверке или завершена"
        )
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN,
                            detail=exeption_delail)

    ipr = await ipr_crud.get_ipr_by_id(task.ipr_id, session)
    notification_supervisor = Notification(
        title="Задача выполнена",
        brief_text="Сотрудник выполнил задачу. Пожалуйста, ознакомьтесь с результатом.",
        date=date.today(),
        ipr_id=ipr.id,
        user_id=ipr.supervisor_id,
        task_id=task.id,
    )

    await notification_crud.create_notification(notification_supervisor,
                                                session)

    if ipr.mentor_id:
        notification_mentor = Notification(
            title="Задача выполнена",
            brief_text="Сотрудник выполнил задачу. Пожалуйста, ознакомьтесь с результатом.",
            date=date.today(),
            ipr_id=ipr.id,
            user_id=ipr.mentor_id,
            task_id=task.id,
        )

        await notification_crud.create_notification(notification_mentor,
                                                    session)

    await task_crud.patch_task_awaiting_review(id, session)
    return JSONResponse(status_code=HTTPStatus.OK,
                        content={"message": "Задача удалена"})
