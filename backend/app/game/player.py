class Player:

    def __init__(self, user_id):

        self.user_id = user_id

        self.position = None

        self.starting_position = None

        self.traps_remaining = []

        self.lives = 3

        self.alive = True
