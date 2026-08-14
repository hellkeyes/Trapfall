from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from backend.app.websocket.manager import connection_manager
from backend.app.websocket.handlers import handle_message
from backend.app.auth.jwt import decode_access_token
from backend.rooms.manager import manager

import asyncio

router = APIRouter(tags=["WebSocket"])


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str):
    payload = decode_access_token(token)

    if payload is None:
        await websocket.close()
        return

    user_id = payload["user_id"]

    await connection_manager.connect(user_id, websocket, room_code)

    try:
        while True:
            data = await websocket.receive_json()

            await handle_message(user_id, data)

    except WebSocketDisconnect:
        await connection_manager.disconnect(user_id)


@router.websocket("/ws/rooms/{room_code}")
async def rooms_socket(websocket: WebSocket, room_code: str, token: str):
    print("WEBSOCKET HIT", room_code)
    payload = decode_access_token(token)

    if payload is None:
        await websocket.close()
        return

    user_id = payload["user_id"]

    game = manager.rooms.get(room_code)

    if game is None:
        await websocket.close()
        return

    # Check player belongs to room
    if (
        game.player_a is None or 
        game.player_a.user_id != user_id
    ) and (
        game.player_b is None or 
        game.player_b.user_id != user_id
    ):
        await websocket.close()
        return

    await connection_manager.connect(user_id, websocket, room_code)

    try:
        while True:
            data = await websocket.receive_json()

            print("RECEIVED:", data)

            try:
                await handle_message(user_id, data, websocket)

            except Exception as e:
                print("MESSAGE ERROR:", repr(e))

                await websocket.send_json({
                    "type": "ERROR",
                    "message": str(e)
                })

    except WebSocketDisconnect:

        print(f"PLAYER {user_id} DISCONNECTED")

        await connection_manager.disconnect(
            room_code,
            user_id
        )

        asyncio.create_task(
            reconnect_handler(room_code, user_id)
        )



async def reconnect_handler(room_code, user_id):
    print(f"WAITING FOR PLAYER {user_id} TO RECONNECT")

    await asyncio.sleep(60)

    if user_id not in connection_manager.connections:

        print(f"PLAYER {user_id} DID NOT RECONNECT")

    else:
        print(f"PLAYER {user_id} RECONNECTED")

