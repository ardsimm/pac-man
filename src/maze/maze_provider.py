from enum import IntEnum

from mazegenerator import MazeGenerator

CORRIDOR = 16


class Dir(IntEnum):
    N = 1
    E = 2
    S = 4
    W = 8


DELTA: dict[Dir, tuple[int, int]] = {
    Dir.N: (-1, 0),
    Dir.E: (0, 1),
    Dir.S: (1, 0),
    Dir.W: (0, -1),
}


class MazeProvider:
    def __init__(self, size: tuple[int, int]) -> None:
        self._maze_gen: MazeGenerator = MazeGenerator(size, perfect=False)

    def _maze_to_tiles(self) -> list[list[bool]]:
        H, W = self.size
        tiles = [[True] * (2 * W + 1) for _ in range(2 * H + 1)]

        for y in range(H):
            for x in range(W):
                cell = self.maze[y][x]
                if cell == 15:
                    continue
                tiles[2 * y + 1][2 * x + 1] = False
                if not cell & Dir.E:
                    tiles[2 * y + 1][2 * x + 2] = False
                if not cell & Dir.S:
                    tiles[2 * y + 2][2 * x + 1] = False
        return tiles

    def _tiles_walls(self, tiles: list[list[bool]]) -> list[list[int]]:
        H, W = len(tiles), len(tiles[0])

        def is_wall(r: int, c: int) -> bool:
            return 0 <= r < H and 0 <= c < W and tiles[r][c]

        def get_value(r: int, c: int) -> int:
            value = 0
            for d, (dy, dx) in DELTA.items():
                if is_wall(r + dy, c + dx):
                    value |= d
            return value

        return [
            [get_value(r, c) if tiles[r][c] else CORRIDOR for c in range(W)]
            for r in range(H)
        ]

    def generate(self, seed: int = 42) -> None:
        self._maze_gen.generate(seed)
        self._tile_maze = self._tiles_walls(self._maze_to_tiles())

    @property
    def tile_maze(self) -> list[list[int]]:
        return self._tile_maze

    @property
    def maze(self) -> list[list[int]]:
        return self._maze_gen.maze

    @property
    def size(self) -> tuple[int, int]:
        """size[0] = Height, size[1] = Width"""
        return len(self.maze), len(self.maze[0])
