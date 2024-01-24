from fastapi import APIRouter

from app.api.endpoints import notifications_router, ipr_router, user_router


main_router = APIRouter(prefix="/api/v1")
main_router.include_router(ipr_router, prefix="/mentor/iprs/ipr", tags=["ИПР"])
main_router.include_router(notifications_router, tags=["Уведомления"])
main_router.include_router(user_router, tags=["Авторизация и аутентификация"])
