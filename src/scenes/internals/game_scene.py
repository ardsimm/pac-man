import random
from typing import List, Optional, Set, Tuple

import numpy as np
import pygame

from src.config.config import Config
from src.entities.behaviors.pacman_behavior import pacman_behavior
from src.entities.behaviors.utils import can_reach
from src.entities.pacman import Pacman
from src.enums import Direction
from src.event.event import Event
from src.event.event_id import EventId
from src.event.game_event import GameEvent
from src.event.navigation_event import NavigationEvent
from src.event.system_event import SystemEvent
from src.event.user_event import UserEvent
from src.maze.maze_provider import CORRIDOR, MazeProvider
from src.scenes.scene import Scene
from src.scenes.view.game_view import GameView
from src.ui import Box, Button, Drawable, Maze
from src.ui.base import Sprite


class GameScene(Scene):

    view: GameView
    tick_count: int
    pacman_desired_direction: Optional[Direction] = None

    def __init__(self, config: Config) -> None:
        super().__init__(config)

        self.tick_count = 0
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
                behavior=pacman_behavior,
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
                self.view.maze,
                self.view.pac_gums,
                self.view.super_pac_gums,
            ),
            Button(
                "ntm",
                Box(x=10, y=10, width=8, height=3),
                2,
                (255, 255, 255, 255),
            ),
            Sprite(
                f"{self.view.pacman.sprite}/right",
                self.view.pacman.x,
                self.view.pacman.y,
                1,
                1,
            ),
        ]

    def __update_pacman(self, events: List[UserEvent]) -> None:
        for event in events:
            if event.event_id == EventId.MOVE_UP:
                self.pacman_desired_direction = Direction.UP
            elif event.event_id == EventId.MOVE_RIGHT:
                self.pacman_desired_direction = Direction.RIGHT
            elif event.event_id == EventId.MOVE_DOWN:
                self.pacman_desired_direction = Direction.DOWN
            elif event.event_id == EventId.MOVE_LEFT:
                self.pacman_desired_direction = Direction.LEFT

        if self.pacman_desired_direction and can_reach(
            self.view.maze,
            (self.view.pacman.x, self.view.pacman.y),
            self.pacman_desired_direction,
        ):
            self.view.pacman.direction = self.pacman_desired_direction
            self.pacman_desired_direction = None

        speed = self.config.pacman_speed
        nx, ny = self.view.pacman.behavior(self.view)
        self.view.pacman.x_step += nx * (speed / 100)
        self.view.pacman.y_step += ny * (speed / 100)
        if abs(self.view.pacman.x_step) >= 1.0:
            self.view.pacman.x += int(self.view.pacman.x_step)
            self.view.pacman.x_step = 0.0
        if abs(self.view.pacman.y_step) >= 1.0:
            self.view.pacman.y += int(self.view.pacman.y_step)
            self.view.pacman.y_step = 0.0

    def update(self, events: List[Event]) -> None:
        user_events: List[UserEvent] = []
        for event in events:
            match event:
                case SystemEvent():
                    if event.pygame_event.type == pygame.KEYDOWN:
                        if event.pygame_event.key in [pygame.K_UP, pygame.K_w]:
                            user_events.append(UserEvent(EventId.MOVE_UP))
                        if event.pygame_event.key in [
                            pygame.K_RIGHT,
                            pygame.K_d,
                        ]:
                            user_events.append(UserEvent(EventId.MOVE_RIGHT))
                        if event.pygame_event.key in [
                            pygame.K_DOWN,
                            pygame.K_s,
                        ]:
                            user_events.append(UserEvent(EventId.MOVE_DOWN))
                        if event.pygame_event.key in [
                            pygame.K_LEFT,
                            pygame.K_a,
                        ]:
                            user_events.append(UserEvent(EventId.MOVE_LEFT))
                case NavigationEvent():
                    pass
                case GameEvent():
                    pass
        self.__update_pacman(user_events)
        self.tick_count += 1
