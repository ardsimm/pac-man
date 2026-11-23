import sys
import numpy as np
import numpy.typing as npt
import pygame

from .backend import Backend

WEB = sys.platform == "emscripten"


class PyGameBackend(Backend):
    def __init__(self) -> None:
        pygame.display.init()
        self._screen: pygame.Surface | None = None
        pygame.init()

    @property
    def _surface(self) -> pygame.Surface:
        if not self._screen:
            raise RuntimeError("set_display() have to be called before")
        return self._screen

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

    def poll_events(self) -> None:
        pass

    def present(self, buff: npt.NDArray[np.uint8]) -> None:
        h, w = buff.shape[:2]
        self._surface.blit(
            pygame.image.frombuffer(buff, (w, h), "RGBA"), (0, 0)
        )
        pygame.display.flip()

    def close(self) -> None:
        pygame.quit()
