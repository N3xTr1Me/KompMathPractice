from typing import Tuple

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

        self.__f = right_side
        self.__domain = Domain(dimensions[0], dimensions[1], basis, right_side)

    # Mass matrix
    def __mass(self) -> MassMatrix:
        return MassMatrix(self.__domain)

    # Stiffness matrix
    def __stiffness(self) -> StiffnessMatrix:
        return StiffnessMatrix(self.__domain)

    def __build_frame(self, xi: Matrix, t: float) -> Frame:
        return Frame(t=t,
                     mass=self.__mass(),
                     stiffness=self.__stiffness(),
                     coefficients=xi)

    # b_n
    def __b(self) -> Matrix:
        # TODO: implement b_n calculation from the guidebook

        return Matrix(self.__domain.rows(), self.__domain.columns(),
                      np.zeroes(self.__domain.rows(), self.__domain.columns()))

    def __k(self, current: Frame, t: float) -> float:
        return current.t() - t

    # Performs a step of algorithm
    def step(self, t: float, current: Frame, previous: Frame) -> Frame:

        M = self.__mass()
        S = self.__stiffness()
        b = self.__b()
        k = self.__k(current, previous.t())

        left_side = M + S * k  # Xi needed here
        right_side = previous.M() * previous.Xi() + b

        # calculations and LUP decomposition and got result_xi
        result_xi = Matrix(self.__domain.rows(), self.__domain.columns())

        # update the temperature values on the field

        next_step = self.__build_frame(xi=result_xi, t=current.t() + t)

        return next_step
