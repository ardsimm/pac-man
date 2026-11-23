from typing import Tuple

import numpy as np
import numpy.typing as npt

from src.enums.direction import Direction
from src.maze.maze_provider import CORRIDOR

direction_coords_map = {
    Direction.UP: (0, -1),
    Direction.RIGHT: (1, 0),
    Direction.DOWN: (0, 1),
    Direction.LEFT: (-1, 0),
}


def can_reach(
    maze: npt.NDArray[np.uint8], coords: Tuple[int, int], direction: Direction
) -> bool:
    maze_h, maze_w = maze.shape

    x, y = coords
    dx, dy = direction_coords_map[direction]

    target_x = x + dx
    target_y = y + dy

    return (
        target_x > 0
        and target_y > 0
        and target_x < maze_w
        and target_y < maze_h
        and maze[target_y, target_x] == CORRIDOR
    )
