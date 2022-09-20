from abc import ABC, abstractmethod

from numpy import array


# A finite element interface
class IFinite(ABC):

    @abstractmethod
    def _set_values(self, f: callable) -> None:
        pass

    @abstractmethod
    def mass(self) -> array:
        pass

    @abstractmethod
    def stiffness(self) -> array:
        pass
