from pathlib import Path
from .config import Config


class ConfigStore:
    @staticmethod
    def load(path: Path) -> Config:
        raise NotImplementedError
