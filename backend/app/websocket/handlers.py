from backend.rooms.manager import manager
from backend.app.websocket.manager import connection_manager

async def handle_message(user_id, data, websocket):
    message_type = data['type']
    game = manager.get_game(user_id)

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
            }
        })

    if message_type == 'MOVE':
        event = game.move_player(user_id, data)

        await connection_manager.broadcast_to_room(game.room_code, event)