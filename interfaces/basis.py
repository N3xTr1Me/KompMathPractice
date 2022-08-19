from abc import ABC, abstractmethod

from typing import Dict


class IBasis(ABC):

    @abstractmethod
    def initialize_basis(self, basis_functions: Dict[callable]) -> None:
        pass

    @abstractmethod
    def phi_1(self) -> callable:
        pass

    @abstractmethod
    def phi_2(self) -> callable:
        pass

    @abstractmethod
    def d_phi_1(self) -> callable:
        pass

    @abstractmethod
    def d_phi_2(self) -> callable:
        pass
