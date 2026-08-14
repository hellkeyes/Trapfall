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


@router.post("/{room_code}/join")   # when i join exisitin room
async def join_room(room_code: str, current_user: User = Depends(get_current_user)):

    game = manager.rooms.get(room_code)

    if game is None:
        raise HTTPException(status_code=404, detail="Room doesn't exist")
    # Existing player reconnecting
    if (game.player_a and game.player_a.user_id == current_user.id):
        return {"message": "Reconnected"}

    if (game.player_b and game.player_b.user_id == current_user.id):
        return {"message": "Reconnected"}

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


@router.get("/{room_code}/game")    # start the game and broadcast message 
async def start_room(room_code: str, current_user: User = Depends(get_current_user)):
    game = manager.rooms.get(room_code)

    if game is None:
        raise HTTPException(status_code=404, detail="Room doesn't exist.")

    if game.player_a is None or game.player_b is None:
        raise HTTPException(status_code=400, detail="Both players must join before the game can start.")

    if game.phase != "WAITING":
        raise HTTPException( status_code=400, detail="Game has already started")

    game.start_game()

    await connection_manager.broadcast_to_room(
        room_code,
        {
            "type": "GAME_STARTED",
            "player_a": {
                "id": game.player_a.user_id,
                "x": 0,
                "y": 0
            },
            "player_b": {
                "id": game.player_b.user_id,
                "x": 9,
                "y": 9
            }
        }
    )

    return {"message": "Game started."}


@router.get('/{room_code}')          # for the lobby 
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
