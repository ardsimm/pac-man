import numpy as np

from src.scenes.adapter import Adapter
from src.scenes.view import View


class GameAdapter(Adapter):

    def adapt_view(self, view: View) -> np.ndarray:
        raise NotImplementedError("Method not implemented")
