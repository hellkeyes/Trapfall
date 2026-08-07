from fastapi import WebSocket

class ConnectionManager:  #only job here is to maintain connection
    def __init__(self):
        self.connections = {}
        self.room_connections = {}

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

    
    # async def broadcast_to_room(self, room_code, message: dict):
    #     sockets = self.room_connections.get(room_code, {})

    #     for websocket in sockets.values():
    #         await websocket.send_json(message)


    async def broadcast_to_room(self, room_code, message):

        print("Broadcasting to:", room_code)

        print(self.room_connections)

        if room_code not in self.room_connections:
            print("No room found")
            return

        for user_id, websocket in self.room_connections[room_code].items():

            print("Sending to", user_id)

            try:
                await websocket.send_json(message)
                print("Success")

            except Exception as e:
                print("FAILED:", e)


connection_manager = ConnectionManager()