from abc import ABC, abstractmethod
from typing import Dict, Literal, Optional

import numpy as np
import numpy.typing as npt

from src.config.config import Config
from src.config.keys import KeyName
from src.event.event import Event

BACKEND = Literal["pygame"]


class Backend(ABC):
    key_map: Dict[str, KeyName]

    @abstractmethod
    def set_display(self, size: tuple[int, int], fullscreen: bool) -> None:
        pass

    @property
    @abstractmethod
    def size(self) -> tuple[int, int]:
        pass

    @abstractmethod
    def get_screen_size(self) -> tuple[int, int]:
        pass

    @abstractmethod
    def present(self, buff: npt.NDArray[np.uint8]) -> None:
        pass

    @abstractmethod
    def poll_events(self) -> list[Event]:
        pass

    @abstractmethod
    def get_keyname(self, code: int) -> Optional[KeyName]:
        pass

    @staticmethod
    def init(backend: BACKEND, config: Config) -> "Backend":
        match backend:
            case "pygame":
                from .pygame_backend import PyGameBackend

                return PyGameBackend(config)
