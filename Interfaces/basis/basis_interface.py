from abc import ABC, abstractmethod

from Data.grid.dot import Dot
from Data.basis.nodal_function import Phi
from Data.basis.nodal_derivative import DPhi


class IBasis(ABC):

    @abstractmethod
    def f(self, index: int, dot: Dot) -> float:
        pass

    @abstractmethod
    def df(self, index: int, dot: Dot) -> float:
        pass

    @abstractmethod
    def phi(self, index: int) -> Phi:
        pass

    @abstractmethod
    def d_phi(self, index: int) -> DPhi:
        pass

    @abstractmethod
    def __call__(self, index: int, derivative: bool = False, dot: Dot = None):
        pass
