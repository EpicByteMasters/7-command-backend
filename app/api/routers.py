from fastapi import APIRouter
from . import notifications_router

main_router = APIRouter(prefix='/api/v1')
main_router.include_router(notifications_router)
