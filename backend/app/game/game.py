from backend.app.game.board import Board
import time
import asyncio
from backend.app.websocket.manager import connection_manager

class Game:
    def __init__(self, room_code):
    
        self.room_code = room_code

        self.player_a = None
        self.player_b = None

        self.board = Board(10)

        self.phase = 'WAITING'

        self.traps = []   # requires coordiante and owner (x, y) : user_id

        self.current_turn = None

        self.phase_ends_at = None

        # self.turn_started_at = None

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
        self.phase = "TRAP_PLACEMENT"
        self.current_turn = "A"
        self.phase_ends_at = time.time() + 60
        print("NEW DEADLINE:", self.phase_ends_at)
        asyncio.create_task(self.phase_timer())


    def place_trap(self, user_id, data):
        print("PLACE TRAP DATA:", data)
        if self.phase != "TRAP_PLACEMENT":
            raise InvalidPhase("You cannot place traps now.")

        x = data["position"]["x"]
        y = data["position"]["y"]

        if not (0 <= x < 10 and 0 <= y < 10):
            raise InvalidMove("Outside board")

        player_traps = sum(1 for trap in self.traps if trap['owner'] == user_id)

        if player_traps >= 8:
            raise InvalidMove("You already placed 8 traps.")

        self.traps.append({"x": x, "y": y, "owner": user_id})

        return {
            "type": "TRAP_PLACED",
            "player_id": user_id,
            "position": {
                "x": x,
                "y": y
            }
        }
        

    def move_player(self, user_id, data):

        if self.phase != "MOVEMENT":
            raise InvalidPhase("You cannot move right now.")

        if self.player_a and self.player_a.user_id == user_id:
            player = self.player_a
            player_side = "A"

        elif self.player_b and self.player_b.user_id == user_id:
            player = self.player_b
            player_side = "B"

        else:
            raise Exception("Player not found")

        if player_side != self.current_turn:
            raise InvalidMove("Not your turn")

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

        if not (0 <= new_x < 10 and 0 <= new_y < 10):    # Check if its within the boundary
            raise InvalidMove("Outside board")

        player.position = (new_x, new_y)

        if self.current_turn == "A":
            self.current_turn = "B"
        else:
            self.current_turn = "A"

        return {
        "type": "PLAYER_MOVED",
        "player_id": user_id,
        "position": {
            "x": player.position[0],
            "y": player.position[1]
            },
        "current_turn": self.current_turn
        }

    async def phase_timer(self):
        print("PHASE TIMER STARTED")
        print("INITIAL DEADLINE:", self.phase_ends_at)

        while True:
            if self.phase_ends_at is not None and time.time() >= self.phase_ends_at:

                if self.phase == "TRAP_PLACEMENT":
                    self.phase = "MEMORIZE"
                    self.phase_ends_at = time.time() + 15

                    print("PHASE TIMER:", self.phase_ends_at)

                    await connection_manager.broadcast_to_room(
                        self.room_code,
                        {
                            "type": "PHASE_CHANGED",
                            "phase": self.phase,
                            "phase_ends_at": self.phase_ends_at
                        }
                    )

                elif self.phase == "MEMORIZE":
                    self.phase = "MOVEMENT"
                    self.phase_ends_at = None

                    print("PHASE TIMER:", self.phase_ends_at)

                    await connection_manager.broadcast_to_room(
                        self.room_code,
                        {
                            "type": "PHASE_CHANGED",
                            "phase": self.phase,
                            "phase_ends_at": self.phase_ends_at
                        }
                    )

            await asyncio.sleep(1)

class RoomIsOccupied(Exception):
    pass

class InvalidMove(Exception):
    pass

class InvalidPhase(Exception):
    pass
