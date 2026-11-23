from __future__ import annotations

from typing import TYPE_CHECKING, List, override

from src.entities.entity import Entity
from src.enums.direction import Direction
from src.event.user_event import UserEvent

if TYPE_CHECKING:
    from src.scenes.view.game_view import GameView


class Pacman(Entity):

    desired_direction: Direction = Direction.UP

    @override
    def update(self, events: List[UserEvent], view: GameView) -> None:
        self.behavior(view)
