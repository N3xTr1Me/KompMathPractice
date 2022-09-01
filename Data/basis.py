from Interfaces.basis_interface import IBasis

from Data.node import Node

from typing import Dict


class Basis(IBasis):
    def __init__(self, functions: Dict[str, callable]):

        if "phi_1" not in functions:
            raise ValueError("phi_1 not found in basis!")
        elif "phi_2" not in functions:
            raise ValueError("phi_2 not found in basis!")
        elif "d_phi_1" not in functions:
            raise ValueError("d_phi_1 not found in basis!")
        elif "d_phi_2" not in functions:
            raise ValueError("d_phi_2 not found in basis!")

        self.__basis = functions

    def phi_1(self, dot: Node, w: int, h: int) -> float:
        return self.__basis["phi_1"](dot.x(), dot.y(), w, h)

    def phi_2(self, dot: Node, w: int, h: int) -> float:
        return self.__basis["phi_2"](dot.x(), dot.y(), w, h)

    def d_phi_1(self, dot: Node, w: int, h: int) -> float:
        return self.__basis["d_phi_1"](dot.x(), dot.y(), w, h)

    def d_phi_2(self, dot: Node, w: int, h: int) -> float:
        return self.__basis["d_phi_2"](dot.x(), dot.y(), w, h)

    def __call__(self, func: str, dot: Node, w: int, h: int) -> float:
        if func in self.__basis:
            return self.__basis[func](dot.x(), dot.y(), w, h)
        else:
            raise ValueError(f"There is no {func} in basis!")
