import numpy as np
import numpy.typing as npt
from mazegenerator import MazeGenerator


class MazeProvider:
    def __init__(self, size: tuple[int, int]) -> None:
        self._maze: MazeGenerator = MazeGenerator(size, perfect=False)

    def generate(self, seed: int = 42) -> None:
        raise NotImplementedError

    @property
    def tile_maze(self) -> npt.NDArray[np.uint8]:
        raise NotImplementedError

    @property
    def maze(self) -> list[list[int]]:
        raise NotImplementedError

    @property
    def size(self) -> tuple[int, int]:
        raise NotImplementedError
