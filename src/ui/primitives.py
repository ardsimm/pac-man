from dataclasses import dataclass

from .box import Box
from .states import ComponentState
from .base import Color, Item, Sprite, Text, Anchor


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
            Sprite(self.texture, self.box.x, self.box.y, self.state),
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
