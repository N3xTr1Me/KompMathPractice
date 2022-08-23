from abc import ABC, abstractmethod
from typing import Dict

from numpy import array


class IDomain(ABC):

    @abstractmethod
    def rows(self) -> int:
        pass

    @abstractmethod
    def columns(self) -> int:
        pass

    @abstractmethod
    def _generate_nodes(self, basis: Dict[str, callable]) -> list:
        pass

    @abstractmethod
    def _map_mesh(self) -> list:
        pass

    @abstractmethod
    def get_mass(self, row: int, column: int) -> array:
        pass

    @abstractmethod
    def get_stiffness(self, row: int, column: int) -> array:
        pass
