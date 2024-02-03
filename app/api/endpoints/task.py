from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user
from app.models.user import User
from app.crud import task_crud

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
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail=exeption_delail)
    await task_crud.patch_task_awaiting_review(id, session)
    return JSONResponse(status_code=HTTPStatus.OK,
                        content={"message": "Задача удалена"})


@router.get(
    "/{id}"
)
async def get_task(id: int, session: AsyncSession = Depends(get_async_session)):
    """Получить задачу по id"""
    task = await task_crud.get(id, session)
    return task
