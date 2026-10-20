from typing import override

from src.entities.entity import Entity
from src.enums.ghost_mode import GhostMode


class Ghost(Entity):

    mode: GhostMode

    @override
    def update(self) -> None:
        raise NotImplementedError("Method not implemented")
