from abc import ABC, abstractmethod

from Data.grid.dot import Dot


class IGlobal(ABC):

    @abstractmethod
    def xk(self) -> float:
        pass

    @abstractmethod
    def yk(self) -> float:
        pass

    @abstractmethod
    def h(self) -> float:
        pass

    @abstractmethod
    def f(self) -> callable:
        pass

    @abstractmethod
    def __call__(self, dot: Dot):
        pass
