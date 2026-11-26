import sys
from typing import List, Optional

import numpy as np
import numpy.typing as npt
import pygame

from src.config.config import Config
from src.config.keys import KeyName
from src.event.event import Event
from src.event.event_id import EventId
from src.event.system_event import KeyDownEvent, SystemEvent

from .backend import Backend

WEB = sys.platform == "emscripten"


class PyGameBackend(Backend):

    config: Config

    def __init__(self, config: Config) -> None:
        pygame.display.init()
        self._screen: pygame.Surface | None = None
        self.key_map = {
            "up": KeyName.UP_ARROW,
            "left": KeyName.LEFT_ARROW,
            "down": KeyName.DOWN_ARROW,
            "right": KeyName.RIGHT_ARROW,
            "space": KeyName.SPACE,
            "escape": KeyName.ESCAPE,
            "w": KeyName.W,
            "a": KeyName.A,
            "s": KeyName.S,
            "d": KeyName.D
        }
        self.config = config
        pygame.init()

    @property
    def _surface(self) -> pygame.Surface:
        if not self._screen:
            raise RuntimeError("set_display() have to be called before")
        return self._screen

    @property
    def size(self) -> tuple[int, int]:
        return self._surface.size

    def set_display(self, size: tuple[int, int], fullscreen: bool) -> None:
        if WEB:
            self._screen = pygame.display.set_mode(size)
        elif fullscreen:
            self._screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            sw, sh = self.get_screen_size()
            ww, wh = min(sw, size[0]), min(sh, size[1])
            self._screen = pygame.display.set_mode((ww, wh))

    def get_screen_size(self) -> tuple[int, int]:
        if WEB:
            from platform import window  # type: ignore[attr-defined]

            return int(window.innerWidth), int(window.innerHeight)
        return pygame.display.get_desktop_sizes()[0]

    def get_keyname(self, code: int) -> Optional[KeyName]:
        try:
            pygame_name = pygame.key.name(code)
            return self.key_map.get(pygame_name)
        except ValueError:
            return None

    def poll_events(self) -> list[Event]:
        events: List[Event] = []
        pygame_events = pygame.event.get()
        for event in pygame_events:
            if event.type == pygame.QUIT:
                events.append(SystemEvent(EventId.QUIT))
            elif event.type == pygame.KEYDOWN:
                keyname = self.get_keyname(event.key)
                if keyname is None:
                    continue
                events.append(KeyDownEvent(keyname=keyname))
        return events

    def present(self, buff: npt.NDArray[np.uint8]) -> None:
        h, w = buff.shape[:2]
        self._surface.blit(
            pygame.image.frombuffer(buff, (w, h), "RGBA"), (0, 0)
        )
        pygame.display.flip()

    def close(self) -> None:
        pygame.quit()
