import numpy as np
import numpy.typing as npt

from PIL import ImageFont, Image, ImageDraw
from functools import lru_cache
from pathlib import Path

from src.ui.base import Color


class FontRenderer:
    def __init__(self) -> None:
        self._load_font = lru_cache()(self._open_font)
        self.create_text = lru_cache(maxsize=128)(self._create_text)

    def _open_font(self, size: int) -> ImageFont.FreeTypeFont:
        font_path = Path("assets/pacman_font.ttf")

        if not font_path.exists():
            font = ImageFont.load_default(size=size)
            if not isinstance(font, ImageFont.FreeTypeFont):
                raise RuntimeError("Pillow version cannot handle freetype")
            return font
        return ImageFont.truetype(
            font_path, size=size, layout_engine=ImageFont.Layout.BASIC
        )

    def _create_text(
        self, label: str, size: int, color: Color
    ) -> npt.NDArray[np.uint8]:
        _font = self._load_font(size)

        left, top, right, bottom = _font.getbbox(label)

        img = Image.new("RGBA", (int(right - left), int(bottom - top)))

        draw = ImageDraw.Draw(img)
        draw.fontmode = "1"
        draw.text((-left, -top), label, font=_font, fill=color)
        return np.asarray(img, dtype=np.uint8)
