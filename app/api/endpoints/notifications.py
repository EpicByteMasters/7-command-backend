import asyncio

from fastapi import WebSocket, Depends
from fastapi.responses import StreamingResponse
from fastapi.routing import APIRouter

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.notifications import check_ipr_dates, user_websockets
from app.models import User


router = APIRouter()
user_check_status = {}


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket,
                             user: User = Depends(current_user)
                             ):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received message from {user.id}: {data}")

            user_check_status[current_user.id] = True if data.lower() == "start" else False
    finally:
        del user_websockets[current_user.id]


@router.get('/notifications',
            response_class=StreamingResponse
            )
async def notifications_endpoint(user: User = Depends(current_user),
                                 session: AsyncSession = Depends(get_async_session)
                                 ):
    async def generate():
        while True:
            await asyncio.sleep(60)

            if user_check_status.get(user.id, False):
                yield await check_ipr_dates(user.id, session)

    return StreamingResponse(generate(), media_type="application/json")
