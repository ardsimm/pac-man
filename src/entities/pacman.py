from typing import override

from src.entities.entity import Entity


class Pacman(Entity):

    @override
    def update(self) -> None:
        raise NotImplementedError("Method not implemented")
