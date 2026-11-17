from typing import Dict, List, Optional

import numpy as np

from src.config.config import Config
from src.event.event import Event
from src.scenes import Scene
from src.scenes.internals.game_scene import GameScene
from src.scenes.internals.ui_scene import UIScene
from src.scenes.scene_type import SceneType
from src.ui.base import Item


class SceneManager:

    __instance: Optional["SceneManager"] = None
    frame: np.ndarray
    __scene_stack: List[Scene]
    __scenes: Dict[SceneType, Scene]

    def __init__(self, config: Config) -> None:
        self.__scenes = {
            SceneType.GAME_SCENE: GameScene(config),
            SceneType.MAIN_MENU_SCENE: UIScene(config),
            SceneType.PAUSE_SCENE: UIScene(config),
            SceneType.GAME_OVER_SCENE: UIScene(config),
            SceneType.GAME_WON_SCENE: UIScene(config),
        }
        self.__scenes[SceneType.GAME_SCENE].z_index = 0
        self.__scene_stack = [self.__scenes[SceneType.GAME_SCENE]]

    def __pop_scene_stack(self) -> Scene:
        poped = self.__scene_stack[0]
        self.__scene_stack.remove(poped)
        for i, stacked_scene in enumerate(self.__scene_stack):
            stacked_scene.z_index = i
        self.__scene_stack.sort(key=lambda scene: scene.z_index)
        return poped

    def __append_scene_stack(self, scene: Scene) -> None:
        scene.z_index = 0
        for i, stacked_scene in enumerate(self.__scene_stack):
            stacked_scene.z_index = i + 1
        self.__scene_stack.append(scene)
        self.__scene_stack.sort(key=lambda scene: scene.z_index)

    def update(self, events: List[Event]) -> None:
        if not len(self.__scene_stack):
            return
        self.__scene_stack[len(self.__scene_stack) - 1].update(events)

    def draw(self) -> List[Item]:
        items: List[Item] = []
        for scene in self.__scene_stack:
            items.extend(scene.draw())
            # TODO: append occlusion plane
        items.reverse()
        return items

    @classmethod
    def get_instance(cls, config: Config) -> "SceneManager":
        if cls.__instance is None:
            cls.__instance = SceneManager(config)
        return cls.__instance

    def stack_scene(self, scene_type: SceneType) -> None:
        scene = self.__scenes[scene_type]
        if scene.is_fullscreen:
            while len(self.__scene_stack):
                self.__pop_scene_stack()
        self.__append_scene_stack(self.__scenes[scene_type])
