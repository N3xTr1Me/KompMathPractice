from abc import ABC, abstractmethod

from Data.node import Node


class IBasis(ABC):

    @abstractmethod
    def phi_1(self, dot: Node, w: int, h: int) -> float:
        pass

    @abstractmethod
    def phi_2(self, dot: Node, w: int, h: int) -> float:
        pass

    @abstractmethod
    def d_phi_1(self, dot: Node, w: int, h: int) -> float:
        pass

    @abstractmethod
    def d_phi_2(self, dot: Node, w: int, h: int) -> float:
        pass
