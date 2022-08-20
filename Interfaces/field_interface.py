from abc import ABC, abstractmethod
from typing import Tuple, Dict

from numpy import array


class IField(ABC):

    @abstractmethod
    def dimensions(self) -> Tuple[int, int]:
        pass

    @abstractmethod
    def elements(self) -> Tuple[int, int]:
        pass

    @abstractmethod
    def _generate_nodes(self, basis: Dict[str, callable]) -> list:
        pass

    @abstractmethod
    def _map_mesh(self) -> list:
        pass

    @abstractmethod
    def get_mass(self, row: int, index: int) -> array:
        pass

    @abstractmethod
    def get_stiffness(self, row: int, index: int) -> array:
        pass
