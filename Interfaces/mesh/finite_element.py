from abc import ABC, abstractmethod

from Data.mesh.node import Node

from numpy import array


# A finite element interface
class IFinite(ABC):

    @abstractmethod
    def mass(self, w: int, h: int) -> array:
        pass

    @abstractmethod
    def stiffness(self, w: int, h: int) -> array:
        pass

    @abstractmethod
    def basis(self, function: str, dot: Node, w: int, h: int) -> float:
        pass

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
