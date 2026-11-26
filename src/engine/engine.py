import time
from typing import List

from src.backend import Backend
from src.config.config import Config
from src.engine.clock import Clock
from src.event import Event, EventId
from src.render.renderer import Renderer
from src.scenes.scene_manager import SceneManager


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
        self.backend = Backend.init("pygame", config)
        self.backend.set_display((1920, 1080), False)
        self.renderer = Renderer(self.backend)

    def tick(self, events: List[Event]) -> None:
        self.scene_manager.update(events)

    def draw(self) -> None:
        self.renderer.render(self.scene_manager.draw())

    def run(self) -> None:
        while self.running:
            events_upstream: List[Event] = []
            events = self.backend.poll_events()
            for event in events:
                if event.event_id == EventId.QUIT:
                    self.running = False
                    return
                else:
                    events_upstream.append(event)
            ticks_count = self.clock.get_ticks()
            if ticks_count > 0:
                for _ in range(ticks_count):
                    self.tick(events_upstream)
                self.draw()
