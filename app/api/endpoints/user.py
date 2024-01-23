from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from fastapi.routing import APIRouter
from app.core.user import auth_backend, fastapi_users

from app.core.db import get_async_session
from app.models.user import User
from app.schemas.user import UserRead, UserCreate

router = APIRouter()


@router.get("/user/{id}", response_model=UserRead)
async def read_users(id: int, session: AsyncSession = Depends(get_async_session)):
    # Получить пользователя из базы данных по идентификатору
    user = await session.execute(select(User).filter(User.id == id))
    user = user.scalar_one()

    return user


router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
