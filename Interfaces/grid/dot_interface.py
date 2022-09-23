from abc import ABC, abstractmethod

from typing import Tuple


class IDot(ABC):

    @abstractmethod
    def x(self) -> float:
        pass

    @abstractmethod
    def y(self) -> float:
        pass

    @abstractmethod
    def coords(self) -> Tuple[float, float]:
        pass
