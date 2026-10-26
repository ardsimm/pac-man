from typing import List, Optional

from src.event.event import Event


class Engine:

    __instance: Optional["Engine"] = None

    @classmethod
    def get_instance(cls) -> "Engine":
        if cls.__instance is None:
            cls.__instance = Engine()
        return cls.__instance

    def tick(self) -> List[Event]:
        raise NotImplementedError("Method not implemented")
