from dataclasses import dataclass, asdict


@dataclass
class PlayerScore:
    name: str
    score: int
    ghost_eaten: int
    pacgum_eaten: int
    super_pacgmum_eaten: int

    @property
    def as_dict(self):
        return asdict(self)
