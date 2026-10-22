import pygame
import numpy as np
import numpy.typing as npt

from itertools import chain

from .texture.texture_manager import TextureManager
from .models import Color


def create_rectangle(h: int, w: int, color: Color) -> np.ndarray:
    sprite = np.empty((h, w, 4), np.uint8)
    sprite[:] = color
    return sprite


def draw(buff: np.ndarray, x: int, y: int, sprite: np.ndarray) -> None:
    h, w = sprite.shape[:2]

    fx0, fy0 = max(x, 0), max(y, 0)
    fx1, fy1 = min(x + w, buff.shape[1]), min(y + h, buff.shape[0])

    if fx0 > fx1 or fy0 > fy1:
        return
    part = sprite[fy0 - y : fy1 - y, fx0 - x : fx1 - x]
    np.copyto(buff[fy0:fy1, fx0:fx1], part, where=part[..., 3:] > 0)


def test():
    pygame.init()
    W, H = 1000, 1000

    tex_manager = TextureManager(128)
    frame = np.zeros((H, W, 4), np.uint8)
    surf = pygame.image.frombuffer(frame, (W, H), "RGBA")
    screen = pygame.display.set_mode((W, H))
    frame[:] = (255, 255, 255, 255)

    tex_manager.set_theme("test_missing")
    assets = tex_manager.theme_assets

    GAP = 20
    step = tex_manager.tile + GAP
    cols = (W - GAP) // step

    images = chain.from_iterable([asset.values() for asset in assets.values()])
    for n, v in enumerate(images):
        x = GAP + (n % cols) * step
        y = GAP + (n // cols) * step
        draw(frame, x, y, v)

    screen.blit(surf)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
    pygame.quit()
