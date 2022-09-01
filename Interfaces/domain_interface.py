from abc import ABC, abstractmethod

from Data.basis import Basis

from numpy import array


class IDomain(ABC):

    @abstractmethod
    def rows(self) -> int:
        pass

    @abstractmethod
    def columns(self) -> int:
        pass

    @abstractmethod
    def _generate_nodes(self, heat_source: callable) -> list:
        pass

    @abstractmethod
    def _map_mesh(self, basis: Basis) -> list:
        pass

    @abstractmethod
    def get_mass(self, row: int, column: int) -> array:
        pass

    @abstractmethod
    def get_stiffness(self, row: int, column: int) -> array:
        pass
