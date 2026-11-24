from typing import List

import numpy as np
import numpy.typing as npt


from src.ui.base import Item, Text, Sprite, TileMap
from src.ui import Anchor
from src.backend import Backend

from .models import Frame
from .texture.texture_manager import TextureManager
from .font import FontRenderer


class Renderer:
    def __init__(self, backend: Backend) -> None:
        self._backend = backend

        w, h = self._backend.size
        self.frame: Frame = np.zeros((h, w, 4), np.uint8)
        self._texture_manager: TextureManager = TextureManager()
        self._font_renderer: FontRenderer = FontRenderer()

    def _get_text_position(
        self, text: Text, rendered: npt.NDArray[np.uint8]
    ) -> tuple[float, float]:
        h, w = rendered.shape[:2]
        box = text.box
        y = box.y + (box.height - h) / 2
        match text.anchor:
            case Anchor.RIGHT:
                x = box.x + box.width - w
            case Anchor.CENTER:
                x = box.x + (box.width - w) / 2
            case _:
                x = box.x
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
                    text = self._font_renderer.create_text(
                        item.label, item.font_size, item.color
                    )
                    x, y = self._get_text_position(item, text)
                    self._draw(self.frame, x, y, text)
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
        self._backend.present(self.frame)
