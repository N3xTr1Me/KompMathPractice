from abc import ABC, abstractmethod

from typing import Dict


class IBasis(ABC):

    def initialize_basis(self, basis_functions: Dict[callable]) -> None:
        pass

    def phi_1(self) -> callable:
        pass

    def phi_2(self) -> callable:
        pass

    def d_phi_1(self) -> callable:
        pass

    def d_phi_2(self) -> callable:
        pass
