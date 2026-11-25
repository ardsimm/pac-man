from src.config.keys import KeyName
from src.event.event import Event
from src.event.event_id import EventId


class SystemEvent(Event):
    def __init__(
        self,
        event_id: EventId,
    ) -> None:
        super().__init__(event_id)


class KeyDownEvent(SystemEvent):
    keyname: KeyName

    def __init__(self, keyname: KeyName) -> None:
        super().__init__(EventId.KEY_DOWN)
        self.keyname = keyname
