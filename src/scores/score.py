from dataclasses import dataclass, asdict


@dataclass
class PlayerScore:
    name: str
    score: int
    ghosts_eaten: int
    pacgums_eaten: int
    super_pacgmums_eaten: int

    @property
    def as_dict(self):
        return asdict(self)
