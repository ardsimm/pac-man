import pygame

from src.event.event import Event
from src.event.event_id import EventId


class SystemEvent(Event):
    pygame_event: pygame.Event

    def __init__(self, event_id: EventId, pygame_event: pygame.Event) -> None:
        super().__init__(event_id)
        self.pygame_event = pygame_event
