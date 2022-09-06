from Data.basis import Basis

from typing import Dict

import numpy as np


class Frame:
    def __init__(self, step: float, matrices: Dict[str, np.array]):

        self.__step = step

        self.__xi = np.array(matrices["xi"])
        self.__m = np.array(matrices["mass"])
        self.__s = np.array(matrices["stiffness"])

        self.__temps = None

    def M(self) -> np.array:
        return self.__m

    def S(self) -> np.array:
        return self.__s

    def Xi(self) -> np.array:
        return self.__xi

    def t(self) -> float:
        return self.__step

    def set_temperatures(self, basis: Basis) -> None:
        h, w = self.__xi.shape[0], self.__xi.shape[1]

        result = np.zeros((w, h), dtype=float)

        for i in range(h - 1):
            for j in range(w - 1):
                # lower-left
                result[i][j] = self.__calculate_t(basis, "lower-left", j, i)

                # upper-left
                result[i + 1][j] = self.__calculate_t(basis, "upper-left", j, i + 1)

                # upper-right
                result[i + 1][j + 1] = self.__calculate_t(basis, "upper-right", j + 1, i + 1)

                # lower-right
                result[i][j + 1] = self.__calculate_t(basis, "lower-right", j + 1, i)

        self.__temps = result

    def __calculate_t(self, basis: Basis, position: str, x: int, y: int) -> float:
        if position == "upper-left":
            return basis.phi_1(x, y, self.__xi.shape[1], self.__xi.shape[0]) * \
                   basis.phi_1(x, y, self.__xi.shape[1], self.__xi.shape[0]) * self.__xi[y][x]

        elif position == "upper-right":
            return basis.phi_2(x, y, self.__xi.shape[1], self.__xi.shape[0]) * \
                   basis.phi_2(x, y, self.__xi.shape[1], self.__xi.shape[0]) * self.__xi[y][x]

        else:
            return basis.phi_1(x, y, self.__xi.shape[1], self.__xi.shape[0]) * \
                   basis.phi_2(x, y, self.__xi.shape[1], self.__xi.shape[0]) * self.__xi[y][x]

    def get_temperatures(self):
        return self.__temps

    def __str__(self):
        result = f"Step № {self.__step}\n"
        if self.__temps is not None:
            result += str(self.__temps) + "\n"

        result += f"Xi coefficients:\n{self.__xi}\n" + f"Mass:\n{self.__m}" + f"Stiffness:\n{self.__s}"

        return result

    def cache(self) -> dict:
        cache = dict()
        cache["step"] = self.__step

        if self.__temps is not None:
            cache["mesh"] = self.__temps.tolist()

        cache["xi"] = self.__xi.tolist()
        cache["mass"] = self.__m.tolist()
        cache["stiffness"] = self.__s.tolist()

        return cache
