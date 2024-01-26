from fastapi.routing import APIRouter

from app.core.user import auth_backend, fastapi_users
from app.schemas.user import UserRead, UserCreate

router = APIRouter()

router.include_router(fastapi_users.get_auth_router(auth_backend),
                      prefix="/auth/jwt")

router.include_router(fastapi_users.get_register_router(UserRead, UserCreate),
                      prefix="/auth")
