from fastapi import APIRouter
from app.api.endpoints.notifications import router as notifications_router

main_router = APIRouter(prefix='/api/v1')
main_router.include_router(notifications_router)
