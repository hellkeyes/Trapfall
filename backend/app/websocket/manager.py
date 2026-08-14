from fastapi import WebSocket

class ConnectionManager:  #only job here is to maintain connection
    def __init__(self):
        self.connections = {}  #user id and their websocket
        self.room_connections = {}  # room code -> their user and respective websocket

    async def connect(self, user_id, websocket, room_code):
        await websocket.accept()

        if user_id in self.connections:
            old_socket = self.connections[user_id]
            for room in self.room_connections.values():
                room.pop(user_id, None)
            await old_socket.close()

        self.connections[user_id] = websocket

        if room_code not in self.room_connections:
            self.room_connections[room_code] = {}

        self.room_connections[room_code][user_id] = websocket

    
    async def disconnect(self, room_code ,user_id):
        if user_id in self.connections:
            del self.connections[user_id]

        if room_code in self.room_connections:
            if user_id in self.room_connections[room_code]:
                del self.room_connections[room_code][user_id]
    

    async def send_to_user(self, user_id, message: dict):
        websocket = self.connections.get(user_id)

        if websocket:
            await websocket.send_json(message)


    async def broadcast_to_room(self, room_code, message):

        if room_code not in self.room_connections:
            return

        for user_id, websocket in self.room_connections[room_code].items():

            try:
                await websocket.send_json(message)

            except Exception as e:
                await self.disconnect(room_code, user_id) # disconeet 


connection_manager = ConnectionManager()