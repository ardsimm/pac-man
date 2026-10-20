from abc import ABC, abstractmethod

from src.enums.direction import Direction


class Entity(ABC):
    x: int
    y: int
    direction: Direction

    @abstractmethod
    def update(self) -> None:
        pass
