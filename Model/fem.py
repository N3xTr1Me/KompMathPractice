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
    def _mass(self) -> MassMatrix:
        return MassMatrix(self.__domain)

    # Stiffness matrix
    def _stiffness(self) -> StiffnessMatrix:
        return StiffnessMatrix(self.__domain)

    def _build_frame(self, xi: Matrix, t: float, mass: MassMatrix, stiff: StiffnessMatrix) -> Frame:
        return Frame(step=t,
                     matrices={"mass": mass.get_data(),
                               "stiffness": stiff.get_data(),
                               "xi": xi.get_data()})

    # b_n
    def _b(self) -> Matrix:
        # TODO: implement b_n calculation from the guidebook

        return Matrix(self.__domain.rows() * 2, self.__domain.columns() * 2,
                      np.zeros((self.__domain.rows() * 2, self.__domain.columns() * 2)))

    def _k(self, current: Frame, t: float) -> float:
        return current.t() - t

    def ksi_n(self, left_side: Matrix, right_side: Matrix):

        first_multiplier = inv(left_side.get_data())
        return Matrix(right_side.rows(), right_side.columns(),
                      data=first_multiplier * right_side.get_data())

    # Performs a step of algorithm
    def step(self, t: float, previous: Frame = None) -> Frame:

        M = self._mass()
        S = self._stiffness()
        b = self._b()
        b = Matrix(self.__domain.rows() * 2, self.__domain.columns() * 2,
                   np.zeros((self.__domain.rows() * 2, self.__domain.columns() * 2)))
        b.change_value(5, 5, 13)

        if previous is not None:
            k = t
            step = previous.t() + t
            right_side = Matrix(self.__domain.rows() * 2, self.__domain.columns() * 2,
                                previous.M() * previous.Xi() + b.get_data())
        else:
            k = 0
            step = 0
            right_side = Matrix(self.__domain.rows() * 2, self.__domain.columns() * 2,
                               np.zeros((self.__domain.rows() * 2, self.__domain.columns() * 2)))

        left_side = M + S * k

        result_ksi = self.ksi_n(left_side, right_side)

        next_step = self._build_frame(xi=result_ksi, t=step, mass=M, stiff=S)

        return next_step
