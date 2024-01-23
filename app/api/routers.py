from fastapi import APIRouter

from . import notifications_router
from . import ipr_router
from . import user_router


main_router = APIRouter(prefix="/api/v1")
main_router.include_router(ipr_router)
main_router.include_router(notifications_router)
main_router.include_router(user_router)
