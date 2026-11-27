import sys
from typing import Any
from functools import lru_cache

import numpy as np
import numpy.typing as npt

from PIL import Image
from pathlib import Path

from ..models import DEFAULT, THEMES, Frame, ThemeNotFound


class TextureManager:
    def __init__(self, theme: str = DEFAULT, root: Path = THEMES) -> None:
        self._root = root
        self._classic_assets = self._load_assets(DEFAULT)
        self.theme, self.theme_assets = DEFAULT, self._classic_assets

        self.get_asset = lru_cache(maxsize=None)(self._get_asset)
        self._cached_bake = lru_cache(maxsize=8)(self._bake_tile_map)

        if theme != DEFAULT:
            self.set_theme(theme)

    def _bake_tile_map(
        self,
        texs_key: str,
        tile_size: tuple[int, int],
        data: bytes,
        shape: tuple[int, ...],
    ) -> npt.NDArray[np.uint8]:
        tile_map = np.frombuffer(data, dtype=np.uint8).reshape(shape)

        tw, th = tile_size
        EMPTY = np.zeros((th, tw, 4), np.uint8)
        walls = np.stack(
            [
                self.get_asset(texs_key, th, tw, v)
                for v in range(16)
            ]
            + [EMPTY]
        )
        # (17, ASSET_SIZE, ASSET_SIZE, 4)
        tw, th = tile_size

        h, w = tile_map.shape
        # Reshape multiplie 2 a 2 on change l ordre de la shape pour que les
        #  valeurs se suivent h * ASSET_SIZE et w * ASSET_SIZE
        # de base : (h, w, T, T, 4) -> (h, T, w, T, 4)
        maze_img = (
            walls[tile_map].transpose(0, 2, 1, 3, 4).reshape(h * th, w * tw, 4)
        )
        return maze_img

    @staticmethod
    def _default_asset(h: int, w: int) -> npt.NDArray[np.uint8]:
        tex = np.full((w, h, 4), (255, 0, 255, 255), dtype=np.uint8)
        tex[0: w // 2, 0: h // 2] = (0, 0, 0, 255)
        tex[w // 2: w, h // 2: h] = (0, 0, 0, 255)
        return tex

    def get_tile_map(
        self,	
        tile_map: npt.NDArray[np.uint8],
        tile_size: tuple[int, int],
        key: str,
    ) -> npt.NDArray[np.uint8]:
        tile_map = tile_map.astype(np.uint8, copy=False)
        return self._cached_bake(
            key, tile_size, tile_map.tobytes(), tile_map.shape
        )

    def _get_asset(
        self, name: str, h: int, w: int, frame: int = 0
    ) -> npt.NDArray[np.uint8]:
        if name not in self.theme_assets:
            return self._default_asset(w, h)
        if frame not in self.theme_assets[name]:
            return self._default_asset(w, h)
        resized_assets = Image.fromarray(
            self.theme_assets[name][frame]
        ).resize((w, h), Image.Resampling.NEAREST)
        return np.array(resized_assets)

    def set_theme(self, name: str) -> None:
        if name == DEFAULT:
            self.get_asset.cache_clear()
            self._cached_bake.cache_clear()
            self.theme, self.theme_assets = DEFAULT, self._classic_assets
            return
        try:
            assets = self._load_assets(name)
        except ThemeNotFound as e:
            print(f"Error: {e}", file=sys.stderr)
            return
        self.get_asset.cache_clear()
        self._cached_bake.cache_clear()
        self.theme, self.theme_assets = name, self._classic_assets | assets

    def _load_png(self, path: Path) -> npt.NDArray[Any]:
        try:
            with Image.open(path) as img:
                rgba = np.array(img.convert("RGBA"))
        except IOError:
            print(f"Failed to load asset: {path.name}", file=sys.stderr)
            return self._default_asset(16, 16)
        return rgba

    def _load_assets(self, name: str) -> dict[str, dict[int, Frame]]:
        theme = self._root / name

        if not name.isidentifier() or not theme.is_dir():
            raise ThemeNotFound(f"thème introuvable : {name}")

        textures: dict[str, dict[int, Frame]] = {}
        for f in theme.rglob("*.png"):
            rel = f.relative_to(theme).with_suffix("").as_posix()
            if f.stem.isdigit():
                key, index = rel.rsplit("/", 1)[0], int(f.stem)
            else:
                key, index = rel, 0
            textures.setdefault(key, {})[index] = self._load_png(f)
        return textures
