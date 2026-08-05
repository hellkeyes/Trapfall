from backend.app.game.tile import Tile


class Board:

    def __init__(self, size):
        self.size = size
        self.tiles = []

        for x in range(size):
            row = []

            for y in range(size):
                tile = Tile(x, y)
                row.append(tile)

            self.tiles.append(row)