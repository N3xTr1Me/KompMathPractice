from typing import Tuple

from numpy.linalg import inv

from Interfaces.model.algorithm import IAlgorithm

from Data.matrices.matrix import Matrix
from Data.matrices.mass_matrix import MassMatrix
from Data.matrices.stiffness_matrix import StiffnessMatrix

from Data.mesh.domain import Domain
from Model.algorithm.frame import Frame

import numpy as np


class FEM(IAlgorithm):
    def __init__(self, dimensions: Tuple[int, int], right_side: callable):
        self.__domain = Domain(dimensions[0], dimensions[1], right_side)
        self.__f = right_side

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
    def _b(self, current: float, previous: float) -> Matrix:
        # TODO: implement b_n calculation from the guidebook

        rows = self.__domain.get_height()

        b_vector = np.zeros((rows, 1))

        for y in range(rows):
            b_vector[y][0] = 0

        return Matrix(rows, 1, b_vector)

    def _k(self, current: Frame, t: float) -> float:
        return current.t() - t

    def _ksi_n(self, left_side: Matrix, right_side: Matrix) -> Matrix:

        left_side.update_data(inv(left_side.get_data()))
        ksi = left_side * right_side.get_data()

        return ksi

    def _ksi_0(self) -> Matrix:


    # Performs a step of algorithm
    def step(self, t: float, previous: Frame = None) -> Frame:

        M = self._mass()
        S = self._stiffness()

        if previous is not None:
            k = t
            step = previous.t() + t
            b = self._b(step, previous.t())
            right_side = Matrix(self.__domain.get_height(), self.__domain.get_width(),
                                previous.M() * previous.Xi() + b.get_data())
        else:
            b = self._b(t, 0)
            k = 0
            step = 0
            right_side = Matrix(self.__domain.get_height(), 1,
                                np.zeros((self.__domain.get_height(), 1)))

        left_side = M + S * k

        result_ksi = self._ksi_n(left_side, right_side)

        next_step = self._build_frame(xi=result_ksi, t=step, mass=M, stiff=S)

        return next_step
