from typing import List

import numpy as np
import numpy.typing as npt

from src.render.viewport import ScaleMode, Viewport
from src.ui.base import Item, Text, Sprite, TileMap
from src.ui import Anchor
from src.backend import Backend
from src.ui.box import Box

from .models import Frame
from .texture.texture_manager import TextureManager
from .font import FontRenderer


class Renderer:
    def __init__(self, backend: Backend) -> None:
        GRID = (40, 40)

        self._backend = backend
        w, h = self._backend.size
        self.frame: Frame = np.zeros((h, w, 4), np.uint8)
        self._texture_manager: TextureManager = TextureManager()
        self._font_renderer: FontRenderer = FontRenderer()
        self.vp = Viewport.compute(self._backend.size, (GRID[0], GRID[1]), ScaleMode.fit)

    def _rect(
	    self, x: float, y: float, w: float, h: float
	) -> tuple[int, int, int, int]:
        x0, y0 = self.vp.to_px(x, y)
        x1, y1 = self.vp.to_px(x + w, y + h)
        return x0, y0, max(x1 - x0, 1), max(y1 - y0, 1)
					

    def _get_text_position(
        self, text: Text, rendered: npt.NDArray[np.uint8]
    ) -> tuple[float, float]:
        h, w = rendered.shape[:2]
        box = text.box
        bx, by, bw, bh = self._rect(box.x, box.y, box.width, box.height)
        y = by + (bh - h) / 2
        match text.anchor:
            case Anchor.RIGHT:
                x = bx + bw - w
            case Anchor.CENTER:
                x = bx + (bw - w) / 2
            case _:
                x = bx
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
        part = sprite[fy0 - y : fy1 - y, fx0 - x : fx1 - x]
        np.copyto(buff[fy0:fy1, fx0:fx1], part, where=part[..., 3:] > 0)

    def render(self, items: List[Item]) -> None:
        self.frame[:] = (0, 0, 0, 255)
        for item in items:
            match item:
                case Text():
                    size = max(round(item.font_size * self.vp.tile[1]), 1)
                    text = self._font_renderer.create_text(
                        item.label, size, item.color
                    )
                    x, y = self._get_text_position(item, text)
                    self._draw(self.frame, x, y, text)
                case Sprite():
                    x, y, w, h = self._rect(item.x, item.y, item.w, item.h)
                    sprite = self._texture_manager.get_asset(
                        item.texture, h, w, item.state
                    )
                    self._draw(self.frame, x, y, sprite)
                case TileMap():
                    bake_map = self._texture_manager.get_tile_map(
                        item.tile_map, self.vp.tile, item.key
                    )
                    self._draw(
                        self.frame, *self.vp.to_px(item.x, item.y), bake_map
                    )
        self._backend.present(self.frame)
