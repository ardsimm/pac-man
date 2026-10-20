from abc import ABC, abstractmethod
from typing import Dict

from src.event.event import Event
from src.scenes.adapter import Adapter
from src.scenes.internals.game_scene import GameScene
from src.scenes.internals.ui_scene import UIScene
from src.scenes.scene_type import SceneType
from src.scenes.view import View


class Scene(ABC):

    __instances: Dict[SceneType, "Scene"] = {}
    adapter: Adapter

    @classmethod
    def get_instance(cls, type: SceneType) -> "Scene":
        if type not in SceneType:
            raise ValueError(f"Invalid scene type {type.name}")
        elif (
            type == SceneType.GAME_SCENE and cls.__instances.get(type) is None
        ):
            cls.__instances[type] = GameScene()
        elif type == SceneType.UI_SCENE and cls.__instances.get(type) is None:
            cls.__instances[type] = UIScene()
        return cls.__instances[type]

    @abstractmethod
    def update(self, events: list[Event]) -> View:
        pass
