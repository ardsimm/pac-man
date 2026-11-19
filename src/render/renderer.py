from pathlib import Path
from typing import List

import numpy as np
import numpy.typing as npt
import pygame
import pygame.freetype

from src.ui.base import Item, Text, Sprite, TileMap
from src.ui import Anchor

from .models import Frame
from .texture.texture_manager import TextureManager


class Renderer:
    def __init__(self, width: int, height: int) -> None:
        self.frame: Frame = np.zeros((height, width, 4), np.uint8)
        self._surf = pygame.image.frombuffer(
            self.frame, (width, height), "RGBA"
        )
        self._screen = pygame.display.set_mode((width, height))
        self._texture_manager: TextureManager = TextureManager()
        pygame.init()
        self._font = self._load_font()
        self._font.antialiased = False

    @staticmethod
    def _load_font() -> pygame.freetype.Font:
        if not Path("assets/pacman_font.ttf").exists():
            return pygame.freetype.Font(pygame.font.get_default_font())
        else:
            return pygame.freetype.Font("assets/pacman_font.ttf")

    def _get_text_position(self, text: Text) -> tuple[float, float]:
        rect = self._font.get_rect(text.label, size=text.font_size)
        box = text.box
        y = box.y + (box.height - rect.height) / 2
        match text.anchor:
            case Anchor.LEFT:
                x = box.x
            case Anchor.RIGHT:
                x = box.x + box.width - rect.width
            case Anchor.CENTER:
                x = box.x + (box.width - rect.width) / 2
        return x, y

    @staticmethod
    def _draw(
        buff: npt.NDArray[np.uint8],
        x: float,
        y: float,
        sprite: npt.NDArray[np.uint8],
    ) -> None:
        h, w = sprite.shape[:2]

        x, y = int(x), int(y)
        fx0, fy0 = max(x, 0), max(y, 0)
        fx1, fy1 = min(x + w, buff.shape[1]), min(y + h, buff.shape[0])

        if fx0 > fx1 or fy0 > fy1:
            return
        part = sprite[fy0 - y: fy1 - y, fx0 - x: fx1 - x]
        np.copyto(buff[fy0:fy1, fx0:fx1], part, where=part[..., 3:] > 0)

    def render(self, items: List[Item]) -> None:
        for item in items:
            match item:
                case Text():
                    self._font.render_to(
                        self._surf,
                        self._get_text_position(item),
                        item.label,
                        item.color,
                        size=item.font_size,
                    )
                case Sprite():
                    self._draw(
                        self.frame,
                        item.x,
                        item.y,
                        self._texture_manager.get_asset(
                            item.texture, item.h, item.w, item.state
                        ),
                    )
                case TileMap():
                    bake_map = self._texture_manager.get_tile_map(
                        item.tile_map, item.tile_size, item.key
                    )
                    self._draw(self.frame, item.x, item.y, bake_map)
        self._screen.blit(self._surf, (0, 0))
        pygame.display.flip()
