from abc import ABC, abstractmethod
from typing import (
    Callable,
    Generic,
    List,
    Tuple,
    TypeVar,
)

from pydantic import BaseModel

# Root
R = TypeVar("R", bound=BaseModel)
# Slice
S = TypeVar("S", bound=BaseModel)


class _View(ABC, Generic[S, R]):
    field_name: str
    __subscriptions: List[Tuple[object, Callable[[object, S], None]]]

    def __init__(self, name: str) -> None:
        super().__init__()
        self.__field_name = name
        self.__subscriptions = []

    def get(self, root: R) -> S:
        return root.__getattribute__(self.__field_name)

    def update(self, root: R, slice: S) -> R:
        update = root.model_copy(update={self.__field_name: slice})
        for subscriber, callback in self.__subscriptions:
            callback(subscriber, update.__getattribute__(self.__field_name))
        return update


class Store(ABC, Generic[R]):
    pass
