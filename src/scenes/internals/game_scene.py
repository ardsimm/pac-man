import random
from typing import List, Set, Tuple

import numpy as np

from src.config.config import Config
from src.entities.pacman import Pacman
from src.enums import Direction
from src.event.event import Event
from src.maze.maze_provider import CORRIDOR, MazeProvider
from src.scenes.scene import Scene
from src.scenes.view.game_view import GameView
from src.ui import Box, Button, Drawable, Maze
from src.ui.base import Sprite


class GameScene(Scene):

    view: GameView

    def __init__(self, config: Config) -> None:
        super().__init__(config)

        maze_provider = MazeProvider.get_instance(
            size=(config.levels[0].width, config.levels[0].height)
        )
        maze_provider.generate(hash(config.levels[0].seed))

        pac_gums = np.array(maze_provider.tile_maze == CORRIDOR).astype(
            np.uint8
        )
        super_pac_gums = np.zeros_like(pac_gums)
        used_coordinates: Set[Tuple[int, int]] = set()

        self.tile_size = 32

        for _ in range(
            min(
                config.levels[0].super_pacgums,
                self.config.levels[0].width * self.config.levels[0].height,
            )
        ):
            new_coord = (
                random.randint(0, maze_provider.size[0] - 1),
                random.randint(0, maze_provider.size[1] - 1),
            )
            while (
                new_coord in used_coordinates
                or not pac_gums[new_coord[0], new_coord[1]]
            ):
                new_coord = (
                    random.randint(0, maze_provider.size[0] - 1),
                    random.randint(0, maze_provider.size[1] - 1),
                )

            used_coordinates.add(new_coord)
            pac_gums[new_coord[0], new_coord[1]] = 0
            super_pac_gums[new_coord[0], new_coord[1]] = 1

        maze_dimension = maze_provider.size

        self.view = GameView(
            pacman=Pacman(
                x=maze_dimension[1] - (1 if not maze_dimension[1] % 2 else 0),
                y=maze_dimension[0],
                direction=Direction.UP,
                personnality=lambda: None,
                sprite="pacman",
                animation_index=0,
            ),
            ghosts=[],
            maze=maze_provider.tile_maze,
            pac_gums=pac_gums,
            super_pac_gums=super_pac_gums,
        )

    def draw(self) -> List[Drawable]:
        return [
            Maze(
                0,
                0,
                self.tile_size,
                self.view.maze,
                self.view.pac_gums,
                self.view.super_pac_gums,
            ),
            Button(
                "ntm",
                Box(x=150, y=150, width=200, height=200),
                64,
                (255, 255, 255, 255),
            ),
            Sprite(
                f"{self.view.pacman.sprite}/right",
                self.view.pacman.x * (self.tile_size),
                self.view.pacman.y * (self.tile_size),
                32,
                32,
            ),
        ]

    def update(self, events: List[Event]) -> None:
        pass
