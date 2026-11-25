from src.event.event import Event
from src.event.event_id import EventId


class GameEvent(Event):

    score: int

    def __init__(self, event_id: EventId, score: int):
        super().__init__(event_id)
