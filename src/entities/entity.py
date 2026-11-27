from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable, List, Tuple

from src.enums.direction import Direction
from src.event.user_event import UserEvent

if TYPE_CHECKING:
    from src.scenes.view.game_view import GameView

DIRECTION_ANIM: dict[Direction, str] = {
    Direction.UP: "up",
    Direction.RIGHT: "right",
    Direction.DOWN: "down",
    Direction.LEFT: "left",
}


@dataclass
class Entity(ABC):
    x: int
    y: int
    direction: Direction
    sprite: str
    animation_index: int
    behavior: Callable[[GameView], Tuple[int, int]]
    x_step: float = 0.0
    y_step: float = 0.0

    @abstractmethod
    def update(self, events: List[UserEvent], view: GameView) -> None:
        pass
