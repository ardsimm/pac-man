from typing import Optional


class SceneManager:

    __instance: Optional["SceneManager"] = None

    @classmethod
    def get_instance(cls) -> "SceneManager":
        if cls.__instance is None:
            cls.__instance = SceneManager()
        return cls.__instance
