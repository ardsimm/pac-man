from dataclasses import dataclass
from enum import StrEnum
from typing import TypeAlias


Size: TypeAlias = tuple[int, int]

class ScaleMode(StrEnum):
	fit = "fit"
	stretch = "stretch"


@dataclass(frozen=True)
class Viewport:
	grid: Size
	window: Size
	tile: Size
	offsets: Size
		
	@classmethod
	def compute(
		cls, windows_size: Size, grid_size: Size, scale_mode: ScaleMode
	) -> "Viewport":
		(w, h), (cols, rows) = windows_size, grid_size
		tw, th = max(w // cols, 1), max(h //  rows, 1)
		if scale_mode == ScaleMode.fit:
			tw = th = min(tw, th)

		return cls(
			grid_size, 
			windows_size, 
			(tw, th), 
			((w - tw * cols) // 2, 
			(h - th * rows) // 2)
		)

	def to_px(self, x: float, y: float) -> tuple[int, int]:
		return (
			self.offsets[0] + round(x * self.tile[0]),
			self.offsets[1] + round(y * self.tile[1])
		)

	