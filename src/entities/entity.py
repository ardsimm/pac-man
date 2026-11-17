from abc import ABC, abstractmethod
from typing import Any, Callable

from pydantic.dataclasses import dataclass

from src.enums.direction import Direction


@dataclass
class Entity(ABC):
    x: int
    y: int
    direction: Direction
    personnality: Callable[[], Any]
    sprite: str
    animation_index: int

    @abstractmethod
    def update(self) -> None:
        pass
