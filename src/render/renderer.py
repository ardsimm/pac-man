from pathlib import Path
from typing import List

import numpy as np
import pygame
import pygame.freetype

from src.ui.base import Item, Text

from .models import Frame
from .texture.texture_manager import TextureManager


class Renderer:
    def __init__(self, width: int, height: int, tile: int = 32) -> None:
        self.frame: Frame = np.zeros((height, width, 4), np.uint8)
        self._surf = pygame.image.frombuffer(
            self.frame, (width, height), "RGBA"
        )
        self._screen = pygame.display.set_mode((width, height))
        self._texture_manager: TextureManager = TextureManager(tile)
        pygame.init()
        self._font = self._load_font()
        self._font.antialiased = False

    @staticmethod
    def _load_font() -> pygame.freetype.Font:
        if not Path("assets/pacman_font.ttf").exists():
            return pygame.freetype.Font(pygame.font.get_default_font())
        else:
            return pygame.freetype.Font("assets/pacman_font.ttf")

    def render(self, items: List[Item]) -> None:
        for item in items:
            match item:
                case Text():
                    self._font.render_to(
                        self._surf,
                        (item.box.x, item.box.y),
                        item.label,
                        item.color,
                        size=item.font_size,
                    )
        self._screen.blit(self._surf, (0, 0))
        pygame.display.flip()
