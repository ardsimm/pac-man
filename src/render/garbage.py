import pygame
import numpy as np
import numpy.typing as npt

from itertools import chain

from .texture.texture_manager import TextureManager
from .models import Color
from src.maze.maze_provider import MazeProvider


def create_rectangle(h: int, w: int, color: Color) -> npt.NDArray[np.uint8]:
    sprite = np.empty((h, w, 4), np.uint8)
    sprite[:] = color
    return sprite


def draw(
    buff: npt.NDArray[np.uint8], x: int, y: int, sprite: npt.NDArray[np.uint8]
) -> None:
    h, w = sprite.shape[:2]

    fx0, fy0 = max(x, 0), max(y, 0)
    fx1, fy1 = min(x + w, buff.shape[1]), min(y + h, buff.shape[0])

    if fx0 > fx1 or fy0 > fy1:
        return
    part = sprite[fy0 - y: fy1 - y, fx0 - x: fx1 - x]
    np.copyto(buff[fy0:fy1, fx0:fx1], part, where=part[..., 3:] > 0)


def test_maze():
    ASSET_SIZE = 32

    tex_manager = TextureManager(ASSET_SIZE)
    tex_manager.set_theme("classic")
    assets = tex_manager.theme_assets
    pygame.init()
    pygame.display.set_mode()
    maze = MazeProvider((20, 20))
    maze.generate()
    tiles = maze.tile_maze

    tiles = np.array(maze.tile_maze, dtype=np.uint8)
    EMPTY = np.zeros((ASSET_SIZE, ASSET_SIZE, 4), np.uint8)
    walls = np.stack(
        [assets["walls"][v] for v in range(16)] + [EMPTY]
    )  # (17, ASSET_SIZE, ASSET_SIZE, 4)
    T = walls.shape[1]

    h, w = tiles.shape
    # Reshape multiplie 2 a 2 on change l ordre de la shape pour que les valeurs se suivent h * ASSET_SIZE et w * ASSET_SIZE
    # de base : (h, w, T, T, 4) -> (h, T, w, T, 4)
    maze_img = walls[tiles].transpose(0, 2, 1, 3, 4).reshape(h * T, w * T, 4)
    maze_surf = pygame.image.frombuffer(
        maze_img, (w * T, h * T), "RGBA"
    ).convert_alpha()

    H, W = 1500, 1500
    frame = np.zeros((H, W, 4), np.uint8)
    surf = pygame.image.frombuffer(frame, (W, H), "RGBA")
    screen = pygame.display.set_mode((W, H))
    frame[:] = (20, 20, 20, 255)

    screen.blit(surf)

    screen.blit(maze_surf, (0, 0))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
    pygame.quit()


def test_texture():
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
