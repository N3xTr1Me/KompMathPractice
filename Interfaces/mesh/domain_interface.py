from abc import ABC, abstractmethod
from typing import Tuple

from numpy import array


class IDomain(ABC):

    @abstractmethod
    def length(self) -> int:
        pass

    @abstractmethod
    def get_load(self, f: callable) -> array:
        pass

    @abstractmethod
    def mass_matrix(self) -> array:
        pass

    @abstractmethod
    def stiffness_matrix(self) -> array:
        pass

    @abstractmethod
    def update_u(self, ksi: array) -> None:
        pass
