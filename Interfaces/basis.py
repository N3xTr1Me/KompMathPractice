from abc import ABC, abstractmethod

from Data.node import Node


class IBasis(ABC):

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
