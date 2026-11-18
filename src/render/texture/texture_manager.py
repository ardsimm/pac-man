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

        if theme != DEFAULT:
            self.set_theme(theme)

    @staticmethod
    def _default_asset(h: int, w: int) -> npt.NDArray[np.uint8]:
        tex = np.full((h, w, 4), (255, 0, 255, 255), dtype=np.uint8)
        tex[0:w // 2, 0:h // 2] = (0, 0, 0, 255)
        tex[w // 2: w, h // 2: h] = (0, 0, 0, 255)
        return tex

    def _get_asset(
        self, name: str, h: int, w: int, frame: int = 0
    ) -> npt.NDArray[np.uint8]:
        if name not in self.theme_assets:
            return self._default_asset(w, h)
        if not self.theme_assets[name].get(frame):
            return self._default_asset(w, h)
        resized_assets = Image.fromarray(
            self.theme_assets[name][frame]
        ).resize((w, h), Image.Resampling.NEAREST)
        return np.array(resized_assets)

    def set_theme(self, name: str) -> None:
        if name == DEFAULT:
            self.get_asset.cache_clear()
            self.theme, self.theme_assets = DEFAULT, self._classic_assets
            return
        try:
            assets = self._load_assets(name)
        except ThemeNotFound as e:
            print(f"Error: {e}")
            return
        self.get_asset.cache_clear()
        self.theme, self.theme_assets = name, self._classic_assets | assets

    def _load_png(self, path: Path) -> npt.NDArray[Any]:
        try:
            with Image.open(path) as img:
                rgba = np.array(img.convert("RGBA"))
        except IOError:
            print(f"Failed to load asset: {path.name}")
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
