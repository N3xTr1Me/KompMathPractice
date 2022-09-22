from abc import ABC, abstractmethod

from numpy import array


class IDomain(ABC):

    @abstractmethod
    def length(self) -> int:
        pass

    @abstractmethod
    def _generate_nodes(self, heat_source: callable) -> list:
        pass

    @abstractmethod
    def get_load(self, f: callable) -> array:
        pass

    @abstractmethod
    def get_mass(self) -> array:
        pass

    @abstractmethod
    def get_stiffness(self) -> array:
        pass

    @abstractmethod
    def update_u(self, ksi: array) -> None:
        pass
