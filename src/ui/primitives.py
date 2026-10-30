from dataclasses import dataclass
from .box import Box


@dataclass
class Button:
    label: str
    box: Box
    texture: str = "ui/button"


@dataclass
class Text:
    label: str
    x: int
    y: int
    font_size: int
