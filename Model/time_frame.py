from Data.matrices.matrix import Matrix
from Data.matrices.mass_matrix import MassMatrix
from Data.matrices.stiffness_matrix import StiffnessMatrix


class Frame:
    def __init__(self, t: float, mass: MassMatrix, stiffness: StiffnessMatrix, coefficients: Matrix):
        self.__t = t

        self.__xi = coefficients
        self.__m = mass
        self.__s = stiffness

    def M(self):
        return self.__m

    def S(self):
        return self.__s

    def Xi(self):
        return self.__xi

    def t(self):
        return self.__t
