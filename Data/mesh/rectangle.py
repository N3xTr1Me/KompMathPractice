from Interfaces.mesh.finite_element import IFinite

from Data.basis.basis import Basis
from Data.mesh.node import Node

import numpy
from scipy.integrate import dblquad


class Rectangle(IFinite):
    def __init__(self, first: Node, second: Node, third: Node, fourth: Node, basis: Basis):
        super(Rectangle, self).__init__()

        # Rectangle vertexes are initialized clockwise starting from the lower_left
        self.__lower_left = first
        self.__lower_right = fourth

        self.__upper_left = second
        self.__upper_right = third

        # initializing element's basis
        self._basis = basis

    # ------------------------------------------------------------------------------------------------------------------

    def basis(self, function: str, dot: Node, w: int, h: int) -> callable:
        return self._basis(function, (dot.x(), dot.y()), w, h)

    def phi_1(self, dot: Node, w: int, h: int) -> float:
        return self._basis.phi_1(dot.x(), dot.y(), w, h)

    def phi_2(self, dot: Node, w: int, h: int) -> float:
        return self._basis.phi_2(dot.x(), dot.y(), w, h)

    def d_phi_1(self, dot: Node, w: int, h: int) -> float:
        return self._basis.d_phi_1(dot.x(), dot.y(), w, h)

    def d_phi_2(self, dot: Node, w: int, h: int) -> float:
        return self._basis.d_phi_2(dot.x(), dot.y(), w, h)

    # returns the local mass matrix of the current finite element
    def mass(self, w: int, h: int) -> numpy.array:
        result = numpy.zeros((2, 2), dtype=float)

        result[0][0] = dblquad(
            lambda x, y: self.phi_1(dot=self.__upper_left, w=x, h=y) * self.phi_1(dot=self.__upper_left, w=x, h=y),
            0, h, lambda x: 0, lambda x: w)[0]

        result[0][1] = dblquad(
            lambda x, y: self.phi_1(dot=self.__upper_right, w=x, h=y) * self.phi_2(dot=self.__upper_right, w=x, h=y),
            0, h, lambda x: 0, lambda x: w)[0]

        result[1][0] = dblquad(
            lambda x, y: self.phi_2(dot=self.__lower_left, w=x, h=y) * self.phi_1(dot=self.__lower_left, w=x, h=y),
            0, h, lambda x: 0, lambda x: w)[0]

        result[1][1] = dblquad(
            lambda x, y: self.phi_2(dot=self.__lower_right, w=x, h=y) * self.phi_2(dot=self.__lower_right, w=x, h=y),
            0, h, lambda x: 0, lambda x: w)[0]
        return result

    # returns the local stiffness matrix of the current finite element
    def stiffness(self, w: int, h: int) -> numpy.array:
        result = numpy.zeros((2, 2), dtype=float)

        result[0][0] = dblquad(
            lambda x, y: self.d_phi_1(self.__upper_left, w=x, h=y) * self.d_phi_1(self.__upper_left, w=x, h=y),
            0, h, lambda x: 0, lambda x: w)[0]

        result[0][1] = dblquad(
            lambda x, y: self.d_phi_1(self.__upper_right, w=x, h=y) * self.d_phi_2(self.__upper_right, w=x, h=y),
            0, h, lambda x: 0, lambda x: w)[0]

        result[1][0] = dblquad(
            lambda x, y: self.d_phi_2(self.__lower_left, w=x, h=y) * self.d_phi_1(self.__lower_left, w=x, h=y),
            0, h, lambda x: 0, lambda x: w)[0]

        result[1][1] = dblquad(
            lambda x, y: self.d_phi_2(self.__lower_right, w=x, h=y) * self.d_phi_2(self.__lower_right, w=x, h=y),
            0, h, lambda x: 0, lambda x: w)[0]

        return result
