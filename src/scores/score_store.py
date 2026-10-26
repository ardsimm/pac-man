from pathlib import Path

from .score import PlayerScore


class ScoreStore:
    @staticmethod
    def save(score: PlayerScore, path: Path) -> None:
        raise NotImplementedError

    @staticmethod
    def load(path: Path) -> None:
        raise NotImplementedError
