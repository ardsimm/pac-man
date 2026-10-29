from typing import Dict, List, Optional

import numpy as np

from src.event.event import Event
from src.scenes import Scene
from src.scenes.internals.game_scene import GameScene
from src.scenes.internals.ui_scene import UIScene
from src.scenes.scene_type import SceneType


class SceneManager:

    __instance: Optional["SceneManager"] = None
    frame: np.ndarray
    __scene_stack: List[Scene]
    __scenes: Dict[SceneType, Scene]
    game_scene: Scene

    def __init__(self) -> None:
        self.game_scene = GameScene()
        self.__scenes = {
            SceneType.GAME_SCENE: GameScene(),
            SceneType.MAIN_MENU_SCENE: UIScene(),
            SceneType.PAUSE_SCENE: UIScene(),
            SceneType.GAME_OVER_SCENE: UIScene(),
            SceneType.GAME_WON_SCENE: UIScene()
        }
        self.__scenes[SceneType.MAIN_MENU_SCENE].z_index = 0
        self.__scene_stack = [self.__scenes[SceneType.MAIN_MENU_SCENE]]

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
        self.__scene_stack.sort(key=lambda scene: scene.z_index)

    def tick(self, events: List[Event]) -> None:
        if not len(self.__scene_stack):
            return
        self.__scene_stack[0].update(events)

    @classmethod
    def get_instance(cls) -> "SceneManager":
        if cls.__instance is None:
            cls.__instance = SceneManager()
        return cls.__instance

    def stack_scene(self, scene_type: SceneType) -> None:
        scene = self.__scenes[scene_type]
        if scene.is_fullscreen:
            while len(self.__scene_stack):
                self.__pop_scene_stack()
        self.__append_scene_stack(self.__scenes[scene_type])
