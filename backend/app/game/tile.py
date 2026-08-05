
class Tile:

    def __init__(self, x, y):

        self.position = (x, y)

        self.trap = False

        self.revealed = False

        self.trap_owner = None
