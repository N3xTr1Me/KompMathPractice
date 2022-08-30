from abc import abstractmethod

from Interfaces.finite_element import IFinite
from Data.node import Node


class IBasis(IFinite):

    @abstractmethod
    def basis(self, function: str) -> callable:
        pass

    @abstractmethod
    def _phi_1(self, dot: Node, w: int, h: int) -> float:
        pass

    @abstractmethod
    def _phi_2(self, dot: Node, w: int, h: int) -> float:
        pass

    @abstractmethod
    def _d_phi_1(self, dot: Node, w: int, h: int) -> float:
        pass

    @abstractmethod
    def _d_phi_2(self, dot: Node, w: int, h: int) -> float:
        pass
