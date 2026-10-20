from typing import override

from src.event.event import Event
from src.scenes.adapter.adapter import Adapter
from src.scenes.adapter.adapter_type import AdapterType
from src.scenes.scene import Scene
from src.scenes.view import View


class UIScene(Scene):

    def __init__(self) -> None:
        self.adapter = Adapter.get_instance(AdapterType.UI_ADAPTER)

    @override
    def update(self, events: list[Event]) -> View:
        raise NotImplementedError("Method not implemented")
