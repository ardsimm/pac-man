from dataclasses import dataclass
from typing import Any, List, Tuple

from src.entities.ghost import Ghost
from src.entities.pacman import Pacman
from src.scenes.view.view import View


@dataclass(frozen=True)
class GameView(View):
    pacman: Pacman
    ghosts: List[Ghost]
    pac_gums: List[Tuple[int, int]]
    super_pac_gums: List[Tuple[int, int]]
    maze: Any
