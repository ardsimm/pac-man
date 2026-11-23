from enum import Enum


class EventId(Enum):

    # System events
    PYGAME_EVENT = 100

    # Game events
    GAME_OVER = 200
    GAME_WON = 201

    # Navigation events
    NAVIGATE_TO = 300
