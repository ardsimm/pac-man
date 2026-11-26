from abc import ABC

from src.event.event_id import EventId


class Event(ABC):

    event_id: EventId

    def __init__(self, event_id: EventId):
        self.event_id = event_id
