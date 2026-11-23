from abc import ABC

from src.event.event_id import EventId
from src.event.event_type import EventType


class Event(ABC):

    event_id: EventId
    type: EventType

    def __init__(self, event_id: EventId):
        self.event_id = event_id
