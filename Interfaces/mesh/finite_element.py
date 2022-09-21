from abc import ABC, abstractmethod

from typing import Dict
from numpy import array

from Data.mesh.node import Node


# A finite element interface
class IFinite(ABC):

    @abstractmethod
    def _set_connections(self, nodes: Dict[str, Node]) -> Dict[str, Node]:
        pass

    @abstractmethod
    def _set_values(self, f: callable) -> None:
        pass

    @abstractmethod
    def mass(self) -> array:
        pass

    @abstractmethod
    def stiffness(self) -> array:
        pass
