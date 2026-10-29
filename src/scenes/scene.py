from abc import ABC, abstractmethod
from typing import List

from src.event.event import Event
from src.scenes.view import View


class Scene(ABC):

    z_index: int
    is_fullscreen: bool

    def __init__(self) -> None:
        super().__init__()
        self.z_index = 0
        self.is_fullscreen = True

    @abstractmethod
    def _tick(self, events: List[Event]) -> View:
        pass

    @abstractmethod
    def _draw(self, view: View) -> None:
        pass

    @abstractmethod
    def update(self, events: list[Event]) -> List[Event]:
        pass
