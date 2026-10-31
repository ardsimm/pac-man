from dataclasses import dataclass


@dataclass
class Box:
    x: float = 0
    y: float = 0
    width: int = 0
    height: int = 0

    def contain(self, pos: tuple[float, float]) -> bool:
        return (
            self.x <= pos[0] <= self.x + self.width
            and self.y <= pos[0] <= self.y + self.height
        )

    @property
    def center(self) -> tuple[float, float]:
        return self.x + self.width / 2, self.y + self.height / 2
