from typing import Tuple


from src.entities.behaviors.utils import can_reach
from src.enums import Direction
from src.scenes.view.game_view import GameView

direction_coords_map = {
    Direction.UP: (0, -1),
    Direction.RIGHT: (1, 0),
    Direction.DOWN: (0, 1),
    Direction.LEFT: (-1, 0),
}


def pacman_behavior(view: GameView) -> Tuple[int, int]:
    pacman = view.pacman
    if not can_reach(view.maze, (pacman.x, pacman.y), pacman.direction):
        return (0, 0)
    return direction_coords_map[pacman.direction]
