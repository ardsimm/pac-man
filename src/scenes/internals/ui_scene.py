from typing import List, override

from src.event.event import Event
from src.scenes.scene import Scene
from src.scenes.view import View


class UIScene(Scene):

    @override
    def _tick(self, events: List[Event]) -> View:
        raise NotImplementedError("Method not implemented")

    @override
    def _draw(self, view: View) -> None:
        raise NotImplementedError("Method not implemented")

    @override
    def update(self, events: list[Event]) -> List[Event]:
        raise NotImplementedError("Method not implemented")
