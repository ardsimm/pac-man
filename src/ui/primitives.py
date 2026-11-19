from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from .box import Box
from .states import ComponentState
from .base import Color, Item, Sprite, Text, Anchor, TileMap


@dataclass
class Button:
    label: str
    box: Box
    text_size: int
    text_color: Color
    state: ComponentState = ComponentState.NORMAL
    texture: str = "ui/button"

    def items(self) -> list[Item]:
        return [
            Sprite(
                self.texture,
                self.box.x,
                self.box.y,
                self.box.height,
                self.box.width,
                self.state,
            ),
            Text(self.label, self.text_size, self.text_color, self.box),
        ]


@dataclass
class Label:
    text: str
    box: Box
    text_size: int
    text_color: Color
    state: ComponentState = ComponentState.NORMAL
    anchor: Anchor = Anchor.CENTER

    def items(self) -> list[Item]:
        return [
            Text(
                self.text,
                self.text_size,
                self.text_color,
                self.box,
                self.anchor,
            )
        ]


@dataclass
class Maze:
    x: int
    y: int
    tile_size: int
    walls: npt.NDArray[np.uint8]
    pac_gums: npt.NDArray[np.uint8]
    super_pac_gums: npt.NDArray[np.uint8]
    walls_texture: str = "walls"
    pac_gum_texture: str = "pacgum"
    super_pac_gum_texture: str = "super_pacgum"

    def _gums(self, mask: npt.NDArray[np.uint8], texture: str) -> list[Item]:
        return [
            Sprite(
                texture,
                self.x + col * self.tile_size,
                self.y + row * self.tile_size,
                self.tile_size,
                self.tile_size,
            )
            for row, col in np.argwhere(mask)
        ]

    def items(self) -> list[Item]:
        return [
            TileMap(
                self.walls_texture, self.x, self.y, self.tile_size, self.walls
            ),
            *self._gums(self.pac_gums, self.pac_gum_texture),
            *self._gums(self.super_pac_gums, self.super_pac_gum_texture),
        ]
