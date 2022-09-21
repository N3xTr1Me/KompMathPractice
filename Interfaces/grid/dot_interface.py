from abc import ABC, abstractmethod

from typing import Tuple


class IDot(ABC):

    @abstractmethod
    def x(self) -> int:
        pass

    @abstractmethod
    def y(self) -> int:
        return self._y

    @abstractmethod
    def coords(self) -> Tuple[float, float]:
        pass
