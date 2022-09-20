from abc import ABC, abstractmethod

from Data.basis.nodal_function import Phi
from Data.basis.nodal_derivative import DPhi


class IBasis(ABC):

    @abstractmethod
    def f(self, x: float, y: float) -> float:
        pass

    @abstractmethod
    def df(self, x: float, y: float) -> float:
        pass

    @abstractmethod
    def phi(self) -> Phi:
        pass

    @abstractmethod
    def d_phi(self) -> DPhi:
        pass

    @abstractmethod
    def __call__(self, derivative: bool = False, x: float = None, y: float = None) -> float | callable:
        pass
