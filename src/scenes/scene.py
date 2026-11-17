from abc import ABC, abstractmethod
from typing import List

from src.config.config import Config
from src.event.event import Event
from src.ui.base import Item


class Scene(ABC):

    z_index: int
    is_fullscreen: bool
    config: Config

    def __init__(self, config: Config) -> None:
        super().__init__()
        self.z_index = 0
        self.is_fullscreen = True
        self.config = config

    @abstractmethod
    def draw(self) -> List[Item]:
        pass

    @abstractmethod
    def update(self, events: List[Event]) -> None:
        pass
