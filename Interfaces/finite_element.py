from abc import ABC, abstractmethod

from numpy import array


# A finite element interface
class IFinite(ABC):

    @abstractmethod
    def mass(self, w: int, h: int) -> array:
        pass

    @abstractmethod
    def stiffness(self, w: int, h: int) -> array:
        pass
