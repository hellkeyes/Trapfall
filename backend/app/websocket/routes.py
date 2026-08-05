from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from backend.app.websocket.manager import connection_manager
from backend.app.websocket.handlers import handle_message
from backend.app.auth.jwt import decode_access_token


router = APIRouter(tags=["WebSocket"])


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str):
    payload = decode_access_token(token)

    if payload is None:
        await websocket.close()
        return

    user_id = payload["user_id"]

    await connection_manager.connect(user_id, websocket)

    try:
        while True:
            data = await websocket.receive_json()

            await handle_message(user_id, data)

    except WebSocketDisconnect:
        connection_manager.disconnect(user_id)


