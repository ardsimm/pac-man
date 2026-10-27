from dataclasses import dataclass, asdict
from typing import Dict, Union


@dataclass
class PlayerScore:
    name: str
    score: int
    ghosts_eaten: int
    pacgums_eaten: int
    super_pacgmums_eaten: int

    @property
    def as_dict(self) -> Dict[str, Union[str, int]]:
        return asdict(self)
