from typing import List

from pydantic import BaseModel
from pydantic.fields import Field


class Level(BaseModel):
    name: str = Field(min_length=2, default="default")
    seed: str = Field(min_length=1, default="42")
    width: int = Field(gt=5, default=50)
    height: int = Field(gt=5, default=50)
    is_perfect: bool = Field(default=False)


class Config(BaseModel):
    levels: List[Level] = Field(default=[Level()])
    lives: int = Field(default=3)
    pacgum: int = Field(default=42)
    points_per_pacgum: int = Field(default=10)
    points_per_super_pacgum: int = Field(default=50)
    points_per_ghost: int = Field(default=200)
    pacman_speed: int = Field(default=10)
