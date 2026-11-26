import time
from typing import List

from src.config.config import Config
from src.engine.clock import Clock
from src.event.event import Event
from src.event.system_event import SystemEvent
from src.render.renderer import Renderer
from src.scenes.scene_manager import SceneManager
from src.backend import Backend
from src.event.event import Event, EventId


class Engine:

    last_ts: int
    running: bool = True
    clock: Clock
    scene_manager: SceneManager
    renderer: Renderer
    backend: Backend

    def __init__(self, config: Config) -> None:
        self.clock = Clock(max_ticks=5, tick_rate=60, ts=time.time_ns())
        self.scene_manager = SceneManager(config=config)
        self.backend = Backend.init("pygame")
        self.backend.set_display((1920, 1080), False)
        self.renderer = Renderer(self.backend)

    def tick(self, events: List[Event]) -> None:
        self.scene_manager.update(events)

    def draw(self) -> None:
        self.renderer.render(self.scene_manager.draw())

    def run(self) -> None:
        while self.running:
            for event in self.backend.poll_events():
                if event.type == EventId.QUIT:
                    self.running = False
            ticks_count = self.clock.get_ticks()
            if ticks_count > 0:
                for _ in range(ticks_count):
                    self.tick(self.backend.poll_events())
                self.draw()
