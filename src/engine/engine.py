import time
from typing import List

import pygame

from src.config.config import Config
from src.engine.clock import Clock
from src.render.renderer import Renderer
from src.scenes.scene_manager import SceneManager


class Engine:

    last_ts: int
    running: bool = True
    clock: Clock
    scene_manager: SceneManager
    renderer: Renderer

    def __init__(self, config: Config) -> None:
        self.clock = Clock(max_ticks=5, tick_rate=60, ts=time.time_ns())
        self.scene_manager = SceneManager(config=config)
        self.renderer = Renderer(
            500, 500
        )

    def tick(self, events: List[pygame.Event]) -> None:
        self.scene_manager.update([])

    def draw(self) -> None:
        self.renderer.render(
            self.scene_manager.draw()
        )

    def run(self) -> None:
        pygame.init()
        while self.running:
            ticks_count = self.clock.get_ticks()
            if ticks_count > 0:
                for _ in range(ticks_count):
                    self.tick(pygame.event.get())
                    self.draw()
