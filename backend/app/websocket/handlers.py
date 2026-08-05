from backend.rooms.manager import manager
from backend.app.websocket.manager import connection_manager

async def handle_message(user_id, data):
    message_type = data['type']
    game = manager.get_game(user_id)

    if message_type == 'MOVE':
        event = game.move_player(user_id, data)

        await connection_manager.broadcast_to_room(game, event)