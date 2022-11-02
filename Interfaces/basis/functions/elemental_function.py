from abc import ABC, abstractmethod

from Data.grid.dot import Dot


class IElemental(ABC):

    @abstractmethod
    def a(self) -> float:
        pass

    @abstractmethod
    def b(self) -> float:
        pass

    @abstractmethod
    def c(self) -> float:
        pass

    @abstractmethod
    def f(self) -> callable:
        pass

    @abstractmethod
    def __call__(self, dot: Dot) -> float:
        pass
