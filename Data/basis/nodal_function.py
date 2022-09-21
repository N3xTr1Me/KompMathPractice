from Interfaces.basis.nodal_basis import INodal
from Data.grid.dot import Dot

from typing import Dict


# Nodal basis function
class Phi(INodal):
    def __init__(self, constants: Dict[str, float]):
        required = ["a", "b", "c"]

        for arg in required:
            if arg not in constants:
                raise ValueError(f"{arg} not found in constants!")

        self.__constants = constants

    def a(self) -> float:
        return self.__constants["a"]

    def b(self) -> float:
        return self.__constants["b"]

    def c(self) -> float:
        return self.__constants["c"]

    def f(self) -> callable:
        return lambda x, y: self.a() * x + self.b() * y + self.c()

    def __call__(self, dot: Dot) -> float:
        return self.f()(dot.x(), dot.y())

    def __str__(self):
        return f"({self.a()})x + ({self.b()})y + ({self.c()})"
