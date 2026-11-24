from abc import ABC, abstractmethod
import numpy as np
import numpy.typing as npt
from typing import Literal

from src.event.event import Event

BACKEND = Literal["pygame"]


class Backend(ABC):
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

    @staticmethod
    def init(backend: BACKEND) -> "Backend":
        match backend:
            case "pygame":
                from .pygame_backend import PyGameBackend

                return PyGameBackend()
