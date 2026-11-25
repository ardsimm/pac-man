from typing import Any

from src.event.event import Event
from src.event.event_id import EventId


class NavigationEvent(Event):

    navigate_to: Any

    def __init__(
        self, navigate_to: Any, event_id: EventId = EventId.NAVIGATE_TO
    ):
        super().__init__(event_id)
        self.navigate_to = navigate_to
