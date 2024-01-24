from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy import select

from app.core.db import AsyncSessionLocal, get_async_session
from app.core.user import auth_backend, fastapi_users
from app.models import User
from app.schemas.user import UserRead, UserCreate

router = APIRouter()


@router.get("/user/{id}", response_model=UserRead)
async def read_users(id: int, session: AsyncSessionLocal = Depends(get_async_session)):
    # Получить пользователя из базы данных по идентификатору
    user = await session.execute(select(User).filter(User.id == id))
    user = user.scalar_one()

    return user


router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
)
