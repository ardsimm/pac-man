from enum import Enum


class EventId(Enum):

    # System events
    KEY_UP = 100
    KEY_DOWN = 101
    QUIT = 102

    # Game events
    GAME_OVER = 200
    GAME_WON = 201

    # Navigation events
    NAVIGATE_TO = 300
