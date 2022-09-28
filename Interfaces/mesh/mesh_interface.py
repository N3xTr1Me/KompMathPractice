from abc import ABC, abstractmethod

from typing import List
from numpy import array

from Data.basis.nodal.nodal_basis import Basis
from Data.grid.dot import Dot
from Data.mesh.node import Node


class IMesh(ABC):

    @abstractmethod
    def width(self) -> int:
        pass

    @abstractmethod
    def height(self) -> int:
        pass

    @abstractmethod
    def k(self) -> int:
        pass

    @abstractmethod
    def get_x(self, element: int, index: int) -> float:
        pass

    @abstractmethod
    def get_y(self, element: int, index: int) -> float:
        pass

    @abstractmethod
    def within_borders(self, dot: Dot) -> bool:
        pass

    @abstractmethod
    def generate_nodes(self, f: callable) -> List[Node]:
        pass

    @abstractmethod
    def map_mesh(self, nodes: List[Node]) -> None:
        pass

    @abstractmethod
    def basis(self, nodes: List[Node]) -> Basis:
        pass

    @abstractmethod
    def get_mass(self, k: int) -> array:
        pass

    @abstractmethod
    def get_stiffness(self, k: int) -> array:
        pass
