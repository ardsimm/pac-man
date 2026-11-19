from typing import Iterable, Protocol

from .base import Item


class Drawable(Protocol):
    def items(self) -> Iterable[Item]: ...
