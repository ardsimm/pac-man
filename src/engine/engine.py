from typing import Optional


class Engine:

    __instance: Optional["Engine"] = None

    @classmethod
    def get_instance(cls) -> "Engine":
        if cls.__instance is None:
            cls.__instance = Engine()
        return cls.__instance
