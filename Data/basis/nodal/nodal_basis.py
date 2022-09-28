from Data.grid.dot import Dot
from Interfaces.basis.basis_interface import IBasis

from Data.basis.nodal.function import Phi
from Data.basis.nodal.derivative import DPhi

from typing import Dict, List


class Basis(IBasis):
    def __init__(self, constants: List[Dict[str, float]]):

        self._functions = []
        self._derivatives = []

        for constant in constants:
            self._functions.append(self._make_function(constant))
            self._derivatives.append(self._make_derivative(constant))

    def _make_function(self, constant: Dict[str, float]):
        return Phi(constant)

    def _make_derivative(self, constant: Dict[str, float]):
        return DPhi(constant)

    def f(self, index: int, dot: Dot) -> float:
        return self._functions[index](dot)

    def df(self, index: int, dot: Dot) -> float:
        return self._derivatives[index](dot)

    def __call__(self, index: int, dot: Dot = None, derivative: bool = False):
        if derivative:
            if dot is not None:
                return self.df(index, dot)

        if dot is not None:
            return self.f(index, dot)
