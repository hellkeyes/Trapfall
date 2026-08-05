from fastapi import WebSocket

class ConnectionManager:  #only job here is to maintain connection
    def __init__(self):
        self.connections = {}

    async def connect(self, user_id, websocket):
        await websocket.accept()

        if user_id in self.connections:
            old_socket = self.connections[user_id]
            await old_socket.close()

        self.connections[user_id] = websocket

    
    async def disconnect(self, user_id):
        if user_id in self.connections:
            del self.connections[user_id]

    
    async def send_to_user(self, user_id, message: dict):
        websocket = self.connections.get(user_id)

        if websocket:
            await websocket.send_json(message)

    
    async def broadcast_to_room(self, game, event):
        if game.player_a:
            await self.send_to_user(game.player_a.id, event)

        if game.player_b:
            await self.send_to_user(game.player_b.id,event)


connection_manager = ConnectionManager()