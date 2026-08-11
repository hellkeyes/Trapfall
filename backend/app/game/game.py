from backend.app.game.board import Board

class Game:
    def __init__(self, room_code):
    
        self.room_code = room_code

        self.player_a = None
        self.player_b = None

        self.board = Board(10)

        self.phase = 'WAITING'

        self.current_turn = None

        self.turn_started_at = None

        self.winner = None

    
    def add_player(self, player):
        if self.player_a is None:
            self.player_a = player
            self.player_a.position = (0, 0)
            self.player_a.starting_position = (0,0)
        elif self.player_b is None:
            self.player_b = player
            self.player_b.position = (9, 9)
            self.player_b.starting_position = (9, 9)
        else:
            raise RoomIsOccupied(f'Game room is full.')


    def start_game(self):
        self.phase = 'TRAP_PLACEMENT'

    
    def move_player(self, user_id, data):
        if self.player_a and self.player_a.user_id == user_id:
            player = self.player_a

        elif self.player_b and self.player_b.user_id == user_id:
            player = self.player_b

        else:
            raise Exception("Player not found")

        direction = data["direction"]

        old_x, old_y = player.position

        if direction == "UP":
            new_x = old_x
            new_y = old_y - 1

        elif direction == "DOWN":
            new_x = old_x
            new_y = old_y + 1

        elif direction == "LEFT":
            new_x = old_x - 1
            new_y = old_y

        elif direction == "RIGHT":
            new_x = old_x + 1
            new_y = old_y

        else:
            raise InvalidMove("Invalid direction")

        # new_position = (data["position"]["x"],data["position"]["y"]) #get current position

        # old_x, old_y = player.position
        # new_x, new_y = new_position

        # if abs(new_x-old_x) > 1 or abs(new_y-old_y) > 1:   # find if move is more than 1 block
        #     raise InvalidMove("Invalid move")

        if not (0 <= new_x < 10 and 0 <= new_y < 10):    # Check if its within the boundary
            raise InvalidMove("Outside board")

        player.position = (new_x, new_y)

        return {
        "type": "PLAYER_MOVED",
        "player_id": user_id,
        "position": {
            "x": player.position[0],
            "y": player.position[1]
            }
        }


class RoomIsOccupied(Exception):
    pass

class InvalidMove(Exception):
    pass
