from typing import TypeAlias
from pathlib import Path
import numpy as np
import numpy.typing as npt

Color: TypeAlias = tuple[int, int, int, int]
THEMES = Path("assets/themes")
DEFAULT = "classic"
Frame: TypeAlias = npt.NDArray[np.uint8]
Frames: TypeAlias = list[Frame]


class ThemeNotFound(Exception):
    pass
