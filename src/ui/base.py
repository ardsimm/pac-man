from dataclasses import dataclass
from typing import TypeAlias
from enum import StrEnum
import numpy as np
import numpy.typing as npt

from .box import Box

Color: TypeAlias = tuple[int, int, int, int]


class Anchor(StrEnum):
    CENTER = "center"
    LEFT = "left"
    RIGHT = "right"


@dataclass
class Rect:
    Box: Box


@dataclass
class Text:
    label: str
    font_size: int
    color: Color
    box: Box
    anchor: Anchor = Anchor.CENTER


@dataclass
class Sprite:
    texture: str
    x: float
    y: float
    state: int = 0


@dataclass
class TileMap:
    key: str
    x: int
    y: int
    tile_map: npt.NDArray[np.uint8]


Item = Text | Sprite
