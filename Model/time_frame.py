import numpy as np

from Data.basis import Basis
from Data.matrices.matrix import Matrix
from Data.matrices.mass_matrix import MassMatrix
from Data.matrices.stiffness_matrix import StiffnessMatrix


class Frame:
    def __init__(self, step: float, mass: MassMatrix, stiffness: StiffnessMatrix, coefficients: Matrix):
        self.__step = step

        self.__xi = coefficients
        self.__m = mass
        self.__s = stiffness

        self.__temps = None

    def M(self) -> MassMatrix:
        return self.__m

    def S(self) -> StiffnessMatrix:
        return self.__s

    def Xi(self) -> Matrix:
        return self.__xi

    def t(self) -> float:
        return self.__step

    def set_temperatures(self, basis: Basis) -> None:
        h, w = self.__xi.rows(), self.__xi.columns()

        result = np.zeros((w, h), dtype=float)

        for i in range(h - 1):
            for j in range(w - 1):
                # lower-left
                result[i][j] = self.calculate_t(basis, "lower-left", j, i)

                # upper-left
                result[i + 1][j] = self.calculate_t(basis, "upper-left", j, i + 1)

                # upper-right
                result[i + 1][j + 1] = self.calculate_t(basis, "upper-right", j + 1, i + 1)

                # lower-right
                result[i][j + 1] = self.calculate_t(basis, "lower-right", j + 1, i)

        self.__temps = Matrix(h, w, result)

    def calculate_t(self, basis: Basis, position: str, x: int, y: int):
        if position == "upper-left":
            return basis.phi_1(x, y, self.__xi.columns(), self.__xi.rows()) * \
                   basis.phi_1(x, y, self.__xi.columns(), self.__xi.rows()) * self.__xi(y, x)

        elif position == "upper-right":
            return basis.phi_2(x, y, self.__xi.columns(), self.__xi.rows()) * \
                   basis.phi_2(x, y, self.__xi.columns(), self.__xi.rows()) * self.__xi(y, x)

        else:
            return basis.phi_1(x, y, self.__xi.columns(), self.__xi.rows()) * \
                   basis.phi_2(x, y, self.__xi.columns(), self.__xi.rows()) * self.__xi(y, x)

    def get_temperatures(self):
        return self.__temps

    def __str__(self):
        result = f"Step # {self.__step}\n"
        if self.__temps is not None:
            result += str(self.__temps) + "\n"

        result += f"Xi coefficients:\n{self.__xi}\n" + f"Mass:\n{self.__m}" + f"Stiffness:\n{self.__s}"

        return result

    def cache(self) -> dict:
        cache = dict()
        cache["step"] = self.__step

        if self.__temps is not None:
            cache["mesh"] = self.__temps.get_data().tolist()

        cache["xi"] = self.__xi.get_data().tolist()
        cache["mass"] = self.__m.get_data().tolist()
        cache["stiffness"] = self.__s.get_data().tolist()

        return cache
