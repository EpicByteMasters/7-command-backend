from fastapi import APIRouter

from app.api.endpoints import (
    auth_router,
    ipr_router,
    notifications_router,
    secondary_router,
    user_router
)

main_router = APIRouter(prefix="/api/v1")
main_router.include_router(ipr_router, prefix="/mentor/iprs/ipr")
main_router.include_router(notifications_router, tags=["Уведомления"])
main_router.include_router(user_router, tags=["Пользователи"])
main_router.include_router(auth_router, tags=["Авторизация и аутентификация"])
main_router.include_router(secondary_router,
                           prefix="/docs",
                           tags=['Стартовая документация'])
