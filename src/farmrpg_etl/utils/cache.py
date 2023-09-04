import typing

_K = typing.TypeVar("_K")
_V = typing.TypeVar("_V")


class FixedSizeCache(typing.Generic[_K, _V], dict[_K, _V]):
    def __init__(self, max_size: int):
        super().__init__()
        self.__max_size = max_size

    def __setitem__(self, key: _K, value: _V) -> None:
        super().__setitem__(key, value)
        if len(self) > self.__max_size:
            oldest_key = next(iter(self.keys()))
            del self[oldest_key]
