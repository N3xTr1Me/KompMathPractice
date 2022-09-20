from Interfaces.basis.basis_interface import IBasis

from Data.basis.nodal_function import Phi
from Data.basis.nodal_derivative import DPhi

from typing import Dict, Tuple


class Basis(IBasis):
    def __init__(self, j: Tuple[float, float], k: Tuple[float, float]):

        constants = self._get_constants(j, k)

        self.__nodal = Phi(constants)
        self.__derivative = DPhi(constants)

    def _get_constants(self, j: Tuple[float, float], k: Tuple[float, float]) -> Dict[str, float]:
        constants = dict()

        constants["a"] = j[0] * k[1] - k[0] * j[1]
        constants["b"] = j[1] - k[1]
        constants["c"] = k[0] - j[0]

        return constants

    def get_a(self) -> float:
        return self.__nodal.a()

    def get_b(self) -> float:
        return self.__nodal.b()

    def get_c(self) -> float:
        return self.__nodal.c()

    def phi(self, x: float, y: float) -> float:
        return self.__nodal(x, y)

    def d_phi(self, x: float, y: float) -> float:
        return self.__derivative(x, y)

    def __call__(self, x: float, y: float, derivative: bool = False) -> float:
        if derivative:
            return self.d_phi(x, y)

        return self.phi(x, y)

    def __str__(self):
        string = "basis [\n"
        string += "nodal: " + str(self.__nodal) + "\n"
        string += "derivative: " + str(self.__derivative) + "\n"
        string += "]"

        return string
