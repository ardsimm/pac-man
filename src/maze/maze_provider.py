import numpy as np
import numpy.typing as npt

from mazegenerator import MazeGenerator
from src.enums import Direction as Dir

_CORRIDOR = 16

_DELTA: dict[Dir, tuple[int, int]] = {
    Dir.UP: (-1, 0),
    Dir.RIGHT: (0, 1),
    Dir.DOWN: (1, 0),
    Dir.LEFT: (0, -1),
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
                if not cell & Dir.RIGHT:
                    tiles[2 * y + 1][2 * x + 2] = False
                if not cell & Dir.DOWN:
                    tiles[2 * y + 2][2 * x + 1] = False
        return tiles

    def _tiles_walls(self, tiles: list[list[bool]]) -> npt.NDArray[np.uint8]:
        H, W = len(tiles), len(tiles[0])

        def is_wall(r: int, c: int) -> bool:
            return 0 <= r < H and 0 <= c < W and tiles[r][c]

        def get_value(r: int, c: int) -> int:
            value = 0
            for d, (dy, dx) in _DELTA.items():
                if is_wall(r + dy, c + dx):
                    value |= d
            return value

        tiles_values = [
            [get_value(r, c) if tiles[r][c] else _CORRIDOR for c in range(W)]
            for r in range(H)
        ]
        return np.array(tiles_values, dtype=np.uint8)

    def generate(self, seed: int = 42) -> None:
        self._maze_gen.generate(seed)
        self._tile_maze = self._tiles_walls(self._maze_to_tiles())

    @property
    def tile_maze(self) -> npt.NDArray[np.uint8]:
        return self._tile_maze

    @property
    def maze(self) -> list[list[int]]:
        return self._maze_gen.maze

    @property
    def size(self) -> tuple[int, int]:
        """size[0] = Height, size[1] = Width"""
        return len(self.maze), len(self.maze[0])
