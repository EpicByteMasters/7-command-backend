from fastapi import Depends
from fastapi.routing import APIRouter

from app.core.db import AsyncSession, get_async_session
from app.core.user import current_user
from app.crud import user_crud
from app.models.user import User
from app.schemas.user import UserRead, UserUpdate

router = APIRouter()


@router.get("/user/me",
            response_model=UserRead,
            dependencies=[Depends(current_user)],
            description="Получить текущего пользователя")
async def get_me(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Получить текущего пользователя."""
    user = await user_crud.get(user.id, session)
    return user


@router.get("/user/{id}",
            response_model=UserRead,
            dependencies=[Depends(current_user)],
            description="Получить пользователя по id")
async def get_user(id: int, session: AsyncSession = Depends(get_async_session)):
    """Получить пользователя из базы данных по идентификатору."""
    user = await user_crud.get(id, session)
    return user


@router.get("/users",
            response_model=list[UserRead],
            dependencies=[Depends(current_user)],
            description="Получить список всех пользователей")
async def list_users(session: AsyncSession = Depends(get_async_session)):
    """Получить список пользователей."""
    user = await user_crud.get_multi(session)
    return user


@router.patch("/user/update/{id}",
              response_model=UserRead,
              dependencies=[Depends(current_user)],
              description="Изменить данные пользователя")
async def get_user(id: int, user_update: UserUpdate, session: AsyncSession = Depends(get_async_session)):
    """Изменить пользователя из базы данных по идентификатору."""
    user = await user_crud.get(id, session)
    user = await user_crud.update(user_update, user, session)
    return user
