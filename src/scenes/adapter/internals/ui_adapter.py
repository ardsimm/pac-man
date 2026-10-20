import numpy as np

from src.scenes.adapter import Adapter
from src.scenes.view import View


class UIAdapter(Adapter):

    def adapt_view(self, frame: np.ndarray, view: View) -> None:
        raise NotImplementedError("Method not implemented")
