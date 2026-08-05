from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.models.user import User
from backend.app.auth.dependencies import get_current_user
from backend.app.game.player import Player
from backend.rooms.manager import Manager

router = APIRouter(prefix="/room", tags=["Rooms"])

manager = Manager()

@router.post('/create')
def create_room(current_user: User = Depends(get_current_user)):
    player = Player(user_id = current_user.id)

    room_code = manager.create_room(player)

    return {'room_code': room_code}


@router.post("/{room_code}/join")
def join_room(room_code: str, current_user: User = Depends(get_current_user)):

    player = Player(user_id=current_user.id)

    manager.join_room(room_code, player)

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