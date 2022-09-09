from Interfaces.mesh.basis_interface import IBasis

from typing import Dict, Tuple


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

    def phi_1(self, x: float, y: float, w: int, h: int) -> float:
        return self.__basis["phi_1"](x, y, w, h)

    def phi_2(self, x: float, y: float, w: int, h: int) -> float:
        return self.__basis["phi_2"](x, y, w, h)

    def d_phi_1(self, x: float, y: float, w: int, h: int) -> float:
        return self.__basis["d_phi_1"](x, y, w, h)

    def d_phi_2(self, x: float, y: float, w: int, h: int) -> float:
        return self.__basis["d_phi_2"](x, y, w, h)

    def __call__(self, func: str, dot: Tuple[float, float], w: int, h: int) -> float:
        if func in self.__basis:
            return self.__basis[func](dot[0], dot[1], w, h)
        else:
            raise ValueError(f"There is no {func} in basis!")
