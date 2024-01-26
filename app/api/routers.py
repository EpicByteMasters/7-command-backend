from fastapi import APIRouter

from app.api.endpoints import notifications_router, ipr_router, iprs_router, user_router, auth_router

main_router = APIRouter(prefix="/api/v1")
main_router.include_router(ipr_router, prefix="/mentor/iprs/ipr", tags=["ИПР"])
main_router.include_router(iprs_router, prefix="/mentor/iprs", tags=["План развития"])
main_router.include_router(notifications_router, tags=["Уведомления"])
main_router.include_router(user_router, tags=["Пользователи"])
main_router.include_router(auth_router, tags=["Авторизация и аутентификация"])
