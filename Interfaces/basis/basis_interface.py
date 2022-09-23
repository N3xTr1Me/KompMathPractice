from abc import ABC, abstractmethod

from Data.grid.dot import Dot

from typing import Dict


class IBasis(ABC):

    @abstractmethod
    def _make_function(self, constant: Dict[str, float]):
        pass

    @abstractmethod
    def _make_derivative(self, constant: Dict[str, float]):
        pass

    @abstractmethod
    def f(self, index: int, dot: Dot) -> float:
        pass

    @abstractmethod
    def df(self, index: int, dot: Dot) -> float:
        pass

    @abstractmethod
    def __call__(self, index: int, dot: Dot = None, derivative: bool = False):
        pass
