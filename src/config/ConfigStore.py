from typing import Protocol, Optional
from config import Config


class ConfigListener(Protocol):
    def on_config_change(self):
        pass


class ConfigStore:
    _config: Optional[Config] = None
    _listeners: list[ConfigListener] = []

    @staticmethod
    def subscribe(listener: ConfigListener):
        raise NotImplementedError

    @staticmethod
    def get_config() -> Config:
        raise NotImplementedError
