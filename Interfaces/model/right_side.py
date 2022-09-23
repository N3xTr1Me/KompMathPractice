from abc import ABC, abstractmethod

from Data.grid.dot import Dot


class IRightSide(ABC):

    @abstractmethod
    def within(self, dot: Dot) -> bool:
        pass

    @abstractmethod
    def __call__(self, dot: Dot) -> float:
        pass
