from typing import List, Optional

import numpy as np

from src.event.event import Event
from src.scenes import Scene


class SceneManager:

    __instance: Optional["SceneManager"] = None
    frame: np.ndarray
    scene_stack: List[Scene]

    def __init__(self) -> None:
        self.scene_stack = []

    def tick(self, events: List[Event]) -> None:
        pass

    @classmethod
    def get_instance(cls) -> "SceneManager":
        if cls.__instance is None:
            cls.__instance = SceneManager()
        return cls.__instance
