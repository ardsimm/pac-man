import time
from typing import List

import pygame

from src.config.config import Config
from src.engine.clock import Clock
from src.event.event import Event
from src.event.system_event import SystemEvent
from src.render.renderer import Renderer
from src.scenes.scene_manager import SceneManager
from src.backend import Backend


class Engine:

    last_ts: int
    running: bool = True
    clock: Clock
    scene_manager: SceneManager
    renderer: Renderer
    backend: Backend

    def __init__(self, config: Config) -> None:
        self.GRID = (40, 40)
        self.clock = Clock(max_ticks=5, tick_rate=60, ts=time.time_ns())
        self.scene_manager = SceneManager(config=config)
        self.backend = Backend.init("pygame")
        self.renderer = Renderer(1920, 1080)

    def __map_pygame_events(self, pygame_events: List[pygame.Event]) -> List[Event]:
        return [
            SystemEvent(
                pygame_event=pygame_event
            )
        for pygame_event in pygame_events
        ]

    def tick(self, events: List[Event]) -> None:
        self.scene_manager.update(events)

    def draw(self) -> None:
        self.renderer.render(self.scene_manager.draw())

    def run(self) -> None:
        pygame.init()
        while self.running:
            events = pygame.event.get()
            filtered_events: List[pygame.Event] = []
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    filtered_events.append(event)
            ticks_count = self.clock.get_ticks()
            if ticks_count > 0:
                for _ in range(ticks_count):
                    self.tick(self.__map_pygame_events(filtered_events))
                self.draw()
