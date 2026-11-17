from dataclasses import dataclass
from typing import TypeAlias
from enum import Enum
import numpy as np
import numpy.typing as npt

from .states import ComponentState
from .box import Box

Color: TypeAlias = tuple[int, int, int, int]


class Anchor(Enum):
    CENTER = "center"
    LEFT = "left"
    RIGHT = "right"


@dataclass
class Rect:
    Box: Box
    color: Color


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
    state: ComponentState = ComponentState.NORMAL


@dataclass
class TileMap:
    key: str
    x: int
    y: int
    tile_map: npt.NDArray[np.uint8]


Item = Text | Sprite | TileMap | Rect
