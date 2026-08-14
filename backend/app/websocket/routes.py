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
    payload = decode_access_token(token)

    if payload is None:
        await websocket.close()
        return

    user_id = payload["user_id"]

    game = manager.rooms.get(room_code)

    if game is None:
        await websocket.send_json({
            "type": "ROOM_NOT_FOUND",
            "message": "This room no longer exists."
        })
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

            try:
                await handle_message(user_id, data, websocket)

            except Exception as e:

                await websocket.send_json({
                    "type": "ERROR",
                    "message": str(e)
                })

    except WebSocketDisconnect:
        await connection_manager.disconnect(room_code, user_id)
        
        asyncio.create_task(reconnect_handler(room_code, user_id))



async def reconnect_handler(room_code, user_id):   # handles if a player joins again within 60 sec

    await asyncio.sleep(60)   # can change the timer if wanted 

    if user_id not in connection_manager.connections:
        await connection_manager.broadcast_to_room(
            room_code,
            {
                "type": "ROOM_TERMINATED",
                "message": "Opponent did not reconnect."
            }
        )

        game = manager.rooms.get(room_code)   # cleaning up dead websockets

        if game:
            if game.player_a:
                await connection_manager.disconnect(
                    room_code,
                    game.player_a.user_id
                )

            if game.player_b:
                await connection_manager.disconnect(
                    room_code,
                    game.player_b.user_id
                )

        manager.delete_room(room_code)  # clean up the room and its room connection to user