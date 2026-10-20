from abc import ABC, abstractmethod
from typing import Dict

import numpy as np

from src.scenes.adapter import AdapterType
from src.scenes.adapter.internals.game_adapter import GameAdapter
from src.scenes.adapter.internals.ui_adapter import UIAdapter
from src.scenes.view import View


class Adapter(ABC):

    __instances: Dict[AdapterType, "Adapter"] = {}

    @classmethod
    def get_instance(cls, type: AdapterType) -> "Adapter":
        if type not in AdapterType:
            raise ValueError(f"Invalid scene type {type.name}")
        elif (
            type == AdapterType.GAME_ADAPTER
            and cls.__instances.get(type) is None
        ):
            cls.__instances[type] = GameAdapter()
        elif (
            type == AdapterType.UI_ADAPTER
            and cls.__instances.get(type) is None
        ):
            cls.__instances[type] = UIAdapter()
        return cls.__instances[type]

    @abstractmethod
    def adapt_view(self, frame: np.ndarray, view: View) -> None:
        pass
