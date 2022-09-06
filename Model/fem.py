from typing import Tuple

from numpy.linalg import inv

from Interfaces.algorithm import IAlgorithm

from Data.matrices.matrix import Matrix
from Data.matrices.mass_matrix import MassMatrix
from Data.matrices.stiffness_matrix import StiffnessMatrix

from Data.basis import Basis
from Data.domain import Domain
from Model.frame import Frame

import numpy as np


class FEM(IAlgorithm):
    def __init__(self, dimensions: Tuple[int, int], basis: Basis, right_side: callable):
        self.__domain = Domain(dimensions[0], dimensions[1], basis, right_side)

    # Mass matrix
    def __mass(self) -> MassMatrix:
        return MassMatrix(self.__domain)

    # Stiffness matrix
    def __stiffness(self) -> StiffnessMatrix:
        return StiffnessMatrix(self.__domain)

    def __build_frame(self, xi: Matrix, t: float, mass: MassMatrix, stiff: StiffnessMatrix) -> Frame:
        return Frame(step=t,
                     matrices={"mass": mass,
                               "stiffness": stiff,
                               "coefficients": xi})

    # b_n
    def __b(self) -> Matrix:
        # TODO: implement b_n calculation from the guidebook

        return Matrix(self.__domain.rows(), self.__domain.columns(),
                      np.zeroes(self.__domain.rows(), self.__domain.columns()))

    def __k(self, current: Frame, t: float) -> float:
        return current.t() - t

    def ksi_n(self, left_side: Matrix, right_side: Matrix):

        first_multiplier = inv(left_side.get_data())
        return first_multiplier * right_side

    # Performs a step of algorithm
    def step(self, t: float, previous: Frame = None) -> Frame:

        M = self.__mass()
        S = self.__stiffness()
        b = self.__b()

        if previous is not None:
            k = t
            right_side = previous.M() * previous.Xi() + b
        else:
            k = 0
            rigt_side = Matrix(self.__domain.rows(), self.__domain.columns(),
                               np.zeros((self.__domain.rows(), self.__domain.columns())))

        left_side = M + S * k

        result_ksi = self.ksi_n(left_side, right_side)

        next_step = self.__build_frame(xi=result_ksi, t=previous.t() + t, mass=M, stiff=S)

        return next_step
