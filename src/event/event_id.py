from enum import Enum


class EventId(Enum):

    # System events
    PYGAME_EVENT = 100

    # Game events
    GAME_OVER = 200
    GAME_WON = 201

    # Navigation events
    NAVIGATE_TO = 300

    # User events
    MOVE_UP = 400
    MOVE_RIGHT = 401
    MOVE_DOWN = 402
    MOVE_LEFT = 403
