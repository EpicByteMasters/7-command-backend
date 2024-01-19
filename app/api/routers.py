from fastapi import APIRouter

from app.api.endpoints.ipr import router as ipr_router


main_router = APIRouter(prefix='/api/v1')
main_router.include_router(ipr_router)
