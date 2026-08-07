from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.models.user import User
from backend.app.auth.dependencies import get_current_user
from backend.app.game.player import Player
from backend.rooms.manager import manager
from backend.app.websocket.manager import connection_manager

router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.post('/create')
def create_room(current_user: User = Depends(get_current_user)):
    player = Player(user_id = current_user.id, username = current_user.username)

    room_code = manager.create_room(player)

    return {'room_code': room_code}


@router.post("/{room_code}/join")
async def join_room(room_code: str, current_user: User = Depends(get_current_user)):

    game = manager.rooms.get(room_code)

    if game is None:
        raise HTTPException(status_code=404, detail="Room doesn't exist")

    if game.player_a and game.player_a.user_id == current_user.id:
        raise HTTPException(status_code=400,detail="You cannot join your own room")

    player = Player(user_id=current_user.id, username = current_user.username)

    manager.join_room(room_code, player)

    await connection_manager.broadcast_to_room(room_code,
        {
            "type": "ROOM_UPDATED",
            "room": {
                "room_code": room_code,
                "player_a": game.player_a.username,
                "player_b": game.player_b.username if game.player_b else None,
                "phase": game.phase
            }
        }
    )

    return {"message": "Joined room"}

@router.post("/{room_code}/start")
def start_room(room_code: str, current_user: User = Depends(get_current_user)):
    game = manager.rooms.get(room_code)

    if game is None:
        raise HTTPException(status_code=404, detail="Room doesn't exist.")

    if game.player_a is None or game.player_b is None:
        return {"message": "Both players must join before the game can start."}

    game.phase = "PLAYING"

    return {"message": "Game started."}


@router.get('/{room_code}')
def get_room(room_code: str):
    game = manager.rooms.get(room_code)

    if game is None:
        raise HTTPException(status_code=404, detail="Room doesn't exist.")

    return {
        "room_code": room_code,
        "player_a": game.player_a.username if game.player_a else None,
        "player_b": game.player_b.username if game.player_b else None,
        "phase": game.phase
    }
