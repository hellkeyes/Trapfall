import string
import secrets
from backend.app.game.game import Game


class Manager:

    def __init__(self):
        self.rooms = {}           # keep active rooms
        self.user_to_room = {}              # which user belongs to which room


    def generate_room_code(self):
        characters = string.ascii_uppercase + string.digits
        return 'TRAP' + '-' +  "".join(secrets.choice(characters) for _ in range(4))


    def create_room(self, player):
        room_code = self.generate_room_code()

        while room_code in self.rooms:
            room_code = self.generate_room_code()

        game = Game(room_code)  # create game
        self.rooms[room_code] = game
        self.user_to_room[player.user_id] = room_code

        game.add_player(player)  # add player a

        return room_code


    def join_room(self, room_code, player):
        if room_code in self.rooms:
            game =  self.rooms[room_code] # get the game
            game.add_player(player) # add player b
            self.user_to_room[player.user_id] = room_code
            return game
        else:
            raise RoomNotFoundError(f"Room '{room_code}' does not exist.")

    
    def get_game(self, user_id):
        if user_id in self.user_to_room:
            room_code = self.user_to_room[user_id]
            game = self.rooms[room_code]
            return game
        else:
            raise RoomNotFoundError(f"User is not currently in any room.")

    
    def delete_room(self, room_code):
        game = self.rooms.get(room_code)

        if game is None:
            return

        if game.player_a:
            self.user_to_room.pop(game.player_a.user_id, None)

        if game.player_b:
            self.user_to_room.pop(game.player_b.user_id, None)
        
        self.rooms.pop(room_code, None)



class RoomNotFoundError(Exception):
    """Raised when a requested room does not exist."""
    pass



manager = Manager()