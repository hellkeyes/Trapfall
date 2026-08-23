from backend.app.websocket.manager import connection_manager
from backend.rooms.manager import manager


async def handle_message(user_id, data, websocket):
    message_type = data['type']
    game = manager.get_game(user_id)

    if user_id == game.player_a.user_id:
        you_are = "A"
    else:
        you_are = "B"

    visible_traps = [
        trap for trap in game.traps
        if trap["owner"] == user_id
    ]

    if message_type == "GET_GAME_STATE":
        await websocket.send_json({
            "type": "GAME_STATE",

            "player_a": {
                "id": game.player_a.user_id,
                "x": game.player_a.position[0],
                "y": game.player_a.position[1]
            },

            "player_b": {
                "id": game.player_b.user_id,
                "x": game.player_b.position[0],
                "y": game.player_b.position[1]
            },

            "you_are": you_are,
            "current_turn": game.current_turn,
            "traps": visible_traps,
            "phase": game.phase,
            "phase_ends_at": game.phase_ends_at
        })

    elif message_type == 'PLACE_TRAP':
        event = game.place_trap(user_id, data)

        # await connection_manager.broadcast_to_room(game.room_code, event)
        await connection_manager.send_to_user(user_id, event)

    elif message_type == 'MOVE':
        event = game.move_player(user_id, data)

        await connection_manager.broadcast_to_room(game.room_code, event)