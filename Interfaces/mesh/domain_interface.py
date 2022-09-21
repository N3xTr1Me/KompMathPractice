from abc import ABC, abstractmethod

from numpy import array


class IDomain(ABC):

    @abstractmethod
    def rows(self) -> int:
        pass

    @abstractmethod
    def columns(self) -> int:
        pass

    @abstractmethod
    def _generate_nodes(self) -> list:
        pass

    @abstractmethod
    def _map_mesh(self, heat_source: callable) -> list:
        pass

    @abstractmethod
    def get_mass(self) -> array:
        pass

    @abstractmethod
    def get_stiffness(self) -> array:
        pass

    @abstractmethod
    def update_u(self, row: int, column: int, value: float):
        pass
