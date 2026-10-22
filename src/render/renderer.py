import pygame
import numpy as np

from .models import Frame
from .texture.texture_manager import TextureManager
from src.scenes.view import View, GameView, UIView

class Renderer:
    def __init__(self, width: int, height: int, tile: int = 32) -> None:
        self.frame: Frame = np.zeros((height, width, 4), np.uint8)
        self._surf = pygame.image.frombuffer(
            self.frame, (width, height), "RGBA"
        )
        self._screen = pygame.display.set_mode((width, height))
        self._texture_manager: TextureManager = TextureManager(tile)
        pygame.init()

    def render(self, view: View) -> None:


