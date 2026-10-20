from typing import Optional

import numpy as np


class SceneManager:

    __instance: Optional["SceneManager"] = None
    frame: np.ndarray

    @classmethod
    def get_instance(cls) -> "SceneManager":
        if cls.__instance is None:
            cls.__instance = SceneManager()
        return cls.__instance
