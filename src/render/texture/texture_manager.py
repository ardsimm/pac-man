import numpy as np
import numpy.typing as npt

from PIL import Image
from pathlib import Path

from ..models import DEFAULT, THEMES, Frame, ThemeNotFound


class TextureManager:
    def __init__(
        self, tile: int, theme: str = DEFAULT, root: Path = THEMES
    ) -> None:
        self.tile = tile
        self._root = root
        self._default_tile = np.full(
            (tile, tile, 4), (255, 0, 255, 255), dtype=np.uint8
        )
        self._classic_theme = self._load_assets(DEFAULT)
        self.theme, self.theme_assets = DEFAULT, self._classic_theme
        if theme != DEFAULT:
            self.set_theme(theme)

    def set_theme(self, name: str) -> None:
        if name == DEFAULT:
            self.theme, self.theme_assets = DEFAULT, self._classic_theme
            return
        try:
            textures = self._load_assets(name)
        except ThemeNotFound as e:
            print(f"Error: {e}")
            return
        self.theme, self.theme_assets = name, textures

    def _load_png(self, path: Path, size: tuple[int, int]) -> npt.NDArray:
        try:
            with Image.open(path) as img:
                resized_img = img.convert("RGBA").resize(
                    size, Image.Resampling.NEAREST
                )
                rgba = np.asarray(resized_img)
        except IOError:
            print(f"Failed to load asset: {path.name}")
            return self._default_tile
        return rgba

    def _load_assets(self, name: str) -> dict[str, dict[int, Frame]]:
        theme = THEMES / name

        if not theme.exists() and not theme.is_dir():
            raise ThemeNotFound(f"Theme {name} is not found: {theme}")

        textures: dict[str, dict[int, Frame]] = {}
        for f in theme.rglob("*.png"):
            rel = f.relative_to(theme).with_suffix("").as_posix()
            if f.stem.isdigit():
                key, index = rel.rsplit("/", 1)[0], int(f.stem)
            else:
                key, index = rel, 0
            textures.setdefault(key, {})[index] = self._load_png(
                f.absolute(), (self.tile, self.tile)
            )
        return textures
