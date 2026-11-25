from __future__ import annotations

from typing import TYPE_CHECKING, List, override

from src.entities.entity import Entity
from src.enums.ghost_mode import GhostMode
from src.event.user_event import UserEvent

if TYPE_CHECKING:
    from src.scenes.view.game_view import GameView


class Ghost(Entity):
    mode: GhostMode

    @override
    def update(self, events: List[UserEvent], view: GameView) -> None:
        raise NotImplementedError("Method not implemented")
