from mazegenerator import MazeGenerator


class MazeProvider:
    def __init__(self, size: tuple[int, int]) -> None:
        self._maze = MazeGenerator(size, perfect=False)

    def generate(self, seed: int = 42):
        pass

    @property
    def tile_maze(self):
        pass

    @property
    def maze(self):
        pass

    @property
    def size(self):
        pass
