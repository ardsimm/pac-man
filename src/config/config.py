from typing import List

from pydantic import BaseModel
from pydantic.fields import Field

from src.config.keys import KeyName


class KeymapConfig(BaseModel):
    move_up: List[str] = Field(
        default=[KeyName.UP_ARROW.value, KeyName.W.value]
    )
    move_left: List[str] = Field(
        default=[KeyName.LEFT_ARROW.value, KeyName.A.value]
    )
    move_down: List[str] = Field(
        default=[KeyName.DOWN_ARROW.value, KeyName.S.value]
    )
    move_right: List[str] = Field(
        default=[KeyName.RIGHT_ARROW.value, KeyName.D.value]
    )
    pause: List[str] = Field(default=[KeyName.SPACE.value])
    menu: List[str] = Field(default=[KeyName.ESCAPE.value])


class DisplayConfig(BaseModel):
    width: int = Field(default=1000)
    height: int = Field(default=800)
    fullscreen: bool = Field(default=False)


class LevelConfig(BaseModel):
    name: str = Field(min_length=2, default="default")
    seed: str = Field(min_length=1, default="42")
    width: int = Field(gt=5, default=15)
    height: int = Field(gt=5, default=15)
    is_perfect: bool = Field(default=False)
    super_pacgums: int = Field(default=16)


class GameConfig(BaseModel):
    lives: int = Field(default=3)
    pacgum: int = Field(default=42)
    points_per_pacgum: int = Field(default=10)
    points_per_super_pacgum: int = Field(default=50)
    points_per_ghost: int = Field(default=200)
    pacman_speed: int = Field(default=10)


class Config(BaseModel):
    levels: List[LevelConfig] = Field(default=[LevelConfig()])
    keymap: KeymapConfig = Field(default=KeymapConfig())
    game: GameConfig = Field(default=GameConfig())
    display: DisplayConfig = Field(default=DisplayConfig())
