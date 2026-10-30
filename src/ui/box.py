from dataclasses import dataclass


@dataclass
class Box:
    x: int = 0
    y: int = 0
    width: int = 0
    height: int = 0

    def contain(self, pos: tuple[int, int]) -> bool:
        return (
            self.x <= pos[0] <= self.x + self.width
            and self.y <= pos[0] <= self.y + self.height
        )

    @property
    def center(self) -> tuple[int, int]:
        return self.x + self.width // 2, self.y + self.height // 2
