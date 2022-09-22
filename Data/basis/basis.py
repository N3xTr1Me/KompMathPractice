from Data.grid.dot import Dot
from Interfaces.basis.basis_interface import IBasis

from Data.basis.nodal_function import Phi
from Data.basis.nodal_derivative import DPhi

from typing import Dict, List


class Basis(IBasis):
    def __init__(self, constants: List[Dict[str, float]]):

        self.__nodal = []
        self.__derivative = []

        for constant in constants:
            self.__nodal.append(Phi(constant))
            self.__derivative.append(DPhi(constant))

    def phi(self, index: int) -> Phi:
        return self.__nodal[index]

    def d_phi(self, index: int) -> DPhi:
        return self.__derivative[index]

    def f(self, index: int, dot: Dot) -> float:
        return self.__nodal[index](dot)

    def df(self, index: int, dot: Dot) -> float:
        return self.__derivative[index](dot)

    def __call__(self, index: int, dot: Dot = None, derivative: bool = False):
        if derivative:
            if dot is not None:
                return self.df(index, dot)

            return self.d_phi(index)

        if dot is not None:
            return self.f(index, dot)

        return self.phi(index)
