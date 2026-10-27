import time
from typing import List

import pygame

from src.engine.clock import Clock


class Engine:

    last_ts: int
    running: bool = True
    clock: Clock

    def __init__(self) -> None:
        self.clock = Clock(max_ticks=5, tick_rate=60, ts=time.time_ns())

    def tick(self, events: List[pygame.Event]) -> None:
        pass

    def run(self) -> None:
        pygame.init()
        while self.running:
            ticks_count = self.clock.get_ticks()
            if ticks_count > 0:
                for _ in range(ticks_count):
                    self.tick(pygame.event.get())
            else:
                print(
                    "Time to next tick:",
                    self.clock.time_to_next_tick / 1_000_000_000,
                )
                time.sleep(
                    max(0, self.clock.time_to_next_tick / 1_000_000_000)
                )
