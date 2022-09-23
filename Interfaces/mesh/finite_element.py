from abc import ABC, abstractmethod

from typing import Dict
from numpy import array

from Data.mesh.node import Node


# A finite element interface
class IFinite(ABC):

    @abstractmethod
    def side(self) -> float:
        pass

    @abstractmethod
    def mass(self) -> array:
        pass

    @abstractmethod
    def stiffness(self) -> array:
        pass
