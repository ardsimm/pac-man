from typing import List

from src.event.event import Event
from src.scenes.scene import Scene
from src.scenes.view.ui_view import UIView
from src.ui import Drawable


class UIScene(Scene):

    view: UIView

    def draw(self) -> List[Drawable]:
        return []

    def update(self, events: List[Event]) -> None:
        pass
