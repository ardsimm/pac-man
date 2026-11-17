from dataclasses import dataclass
from typing import List

import numpy as np
import numpy.typing as npt

from src.entities.ghost import Ghost
from src.entities.pacman import Pacman
from src.scenes.view.view import View


@dataclass(frozen=True)
class GameView(View):
    pacman: Pacman
    ghosts: List[Ghost]
    pac_gums: npt.NDArray[np.uint8]
    super_pac_gums: npt.NDArray[np.uint8]
    maze: npt.NDArray[np.uint8]
