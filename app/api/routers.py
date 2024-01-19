from fastapi import APIRouter

from . import ipr_router


main_router = APIRouter(prefix='/api/v1')
main_router.include_router(ipr_router)
