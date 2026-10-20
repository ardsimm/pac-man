from typing import Any, Dict

from src.event.event_id import EventId


class Event:
    id: EventId
    payload: Dict[str, Any]
