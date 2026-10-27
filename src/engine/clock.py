import time


class Clock:

    last_ts: int
    acc: int
    tick_duration: int
    max_ticks: int

    def __init__(
        self,
        ts: int,
        tick_rate: int,
        max_ticks: int,
    ) -> None:
        self.last_ts = ts
        self.max_ticks = max_ticks
        self.acc = 0
        self.tick_duration = 1_000_000_000 // tick_rate

    @property
    def time_to_next_tick(self) -> int:
        return self.tick_duration - self.acc

    def start(self, ts: int) -> None:
        self.last_ts = ts

    def get_ticks(self) -> int:
        ts = time.time_ns()
        dt = ts - self.last_ts
        self.last_ts = ts
        self.acc += dt
        ticks = 0
        while self.acc >= self.tick_duration and ticks < self.max_ticks:
            ticks += 1
            self.acc -= self.tick_duration
        return ticks
