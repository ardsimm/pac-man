from typing import Dict, List, Optional

import numpy as np

from src.config.config import Config
from src.event.event import Event
from src.event.event_id import EventId
from src.event.system_event import KeyDownEvent
from src.event.user_event import UserEvent
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
    config: Config

    def __init__(self, config: Config) -> None:
        self.config = config
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

    def map_events(
        self, events: List[KeyDownEvent]
    ) -> List[Event]:
        mapped_events: List[Event] = []
        for event in events:
            match event:
                case KeyDownEvent():
                    if event.keyname.value in self.config.keymap.move_up:
                        mapped_events.append(UserEvent(EventId.MOVE_UP))
                    if event.keyname.value in self.config.keymap.move_left:
                        mapped_events.append(UserEvent(EventId.MOVE_LEFT))
                    if event.keyname.value in self.config.keymap.move_right:
                        mapped_events.append(UserEvent(EventId.MOVE_RIGHT))
                    if event.keyname.value in self.config.keymap.move_down:
                        mapped_events.append(UserEvent(EventId.MOVE_DOWN))
                    if event.keyname.value in self.config.keymap.pause:
                        mapped_events.append(UserEvent(EventId.PAUSE))
                    if event.keyname.value in self.config.keymap.menu:
                        mapped_events.append(UserEvent(EventId.MENU))
        return mapped_events

    def update(self, events: List[Event]) -> None:
        if not len(self.__scene_stack):
            return
        self.__scene_stack[len(self.__scene_stack) - 1].update(
            self.map_events([
                event
                for event in events
                if isinstance(event, KeyDownEvent)
            ])
        )

    def draw(self) -> List[Item]:
        items: List[Item] = []
        for scene in self.__scene_stack:
            for drawable in scene.draw():
                items.extend(drawable.items())
            # TODO: append occlusion plane
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
