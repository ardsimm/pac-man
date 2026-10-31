import numpy as np
import numpy.typing as npt
from dataclasses import dataclass

from .box import Box
from .states import ButtonState
from .base import Color, Item, Sprite, Text


@dataclass
class Button:
    label: str
    box: Box
    text_size: int
    text_color: Color
    state: int = ButtonState.NORMAL
    texture: str = "ui/button"

    def items(self) -> list[Item]:
        return [
            Sprite(self.texture, self.box.x, self.box.y, self.state),
            Text(self.label, self.text_size, self.text_color, self.box)
            ]


@dataclass
class TileMap:
    key: str
    x: int
    y: int
    tile_map: npt.NDArray[np.uint8]
