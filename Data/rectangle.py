from Interfaces.finite_element import IFinite
from Interfaces.basis import IBasis
from Data.node import Node

from typing import Dict
import numpy
from scipy.integrate import dblquad


class Rectangle(IFinite, IBasis):
    def __init__(self, first: Node, second: Node, third: Node, fourth: Node, basis_funcs: Dict[str, callable]):
        super(Rectangle, self).__init__()

        # Rectangle vertexes are initialized clockwise starting from the lower_left
        self.__lower_left = first
        self.__lower_right = fourth

        self.__upper_left = second
        self.__upper_right = third

        # --------------------------------------------------------------------------------------------------------------
        # checking the minimal basis requirements
        if "phi_1" not in basis_funcs:
            raise ValueError("phi_1 not found in basis!")
        elif "phi_2" not in basis_funcs:
            raise ValueError("phi_2 not found in basis!")
        elif "d_phi_1" not in basis_funcs:
            raise ValueError("d_phi_1 not found in basis!")
        elif "d_phi_2" not in basis_funcs:
            raise ValueError("d_phi_2 not found in basis!")

        # initializing element's basis
        self._basis = dict()
        for func in basis_funcs:
            self._basis[func] = basis_funcs[func]

    # ------------------------------------------------------------------------------------------------------------------

    def basis(self, function: str) -> callable:
        if function in self._basis:
            return self._basis[function]

        raise KeyError(f"{function} not found among basis functions!")

    def _phi_1(self, dot: Node, w: int, h: int) -> float:
        return self.basis("phi_1")(dot.x(), dot.y(), w, h)

    def _phi_2(self, dot: Node, w: int, h: int) -> float:
        return self.basis("phi_2")(dot.x(), dot.y(), w, h)

    def _d_phi_1(self, dot: Node, w: int, h: int) -> float:
        return self.basis("d_phi_1")(dot.x(), dot.y(), w, h)

    def _d_phi_2(self, dot: Node, w: int, h: int) -> float:
        return self.basis("d_phi_2")(dot.x(), dot.y(), w, h)

    # returns the local mass matrix of the current finite element
    def mass(self, w: int, h: int) -> numpy.array:
        result = numpy.zeros((2, 2), dtype=float)

        result[0][0] = dblquad(
            lambda x, y: self._phi_1(dot=self.__upper_left, w=x, h=y) * self._phi_1(dot=self.__upper_left, w=x, h=y),
            0, h, lambda x: 0, lambda x: w)[0]

        result[0][1] = dblquad(
            lambda x, y: self._phi_1(dot=self.__upper_right, w=x, h=y) * self._phi_2(dot=self.__upper_right, w=x, h=y),
            0, h, lambda x: 0, lambda x: w)[0]

        result[1][0] = dblquad(
            lambda x, y: self._phi_2(dot=self.__lower_left, w=x, h=y) * self._phi_1(dot=self.__lower_left, w=x, h=y),
            0, h, lambda x: 0, lambda x: w)[0]

        result[1][1] = dblquad(
            lambda x, y: self._phi_2(dot=self.__lower_right, w=x, h=y) * self._phi_2(dot=self.__lower_right, w=x, h=y),
            0, h, lambda x: 0, lambda x: w)[0]
        return result

    # returns the local stiffness matrix of the current finite element
    def stiffness(self, w: int, h: int) -> numpy.array:
        result = numpy.zeros((2, 2), dtype=float)

        result[0][0] = dblquad(
            lambda x, y: self._d_phi_1(self.__upper_left, w=x, h=y) * self._d_phi_1(self.__upper_left, w=x, h=y),
            0, h, lambda x: 0, lambda x: w)[0]

        result[0][1] = dblquad(
            lambda x, y: self._d_phi_1(self.__upper_right, w=x, h=y) * self._d_phi_2(self.__upper_right, w=x, h=y),
            0, h, lambda x: 0, lambda x: w)[0]

        result[1][0] = dblquad(
            lambda x, y: self._d_phi_2(self.__lower_left, w=x, h=y) * self._d_phi_1(self.__lower_left, w=x, h=y),
            0, h, lambda x: 0, lambda x: w)[0]

        result[1][1] = dblquad(
            lambda x, y: self._d_phi_2(self.__lower_right, w=x, h=y) * self._d_phi_2(self.__lower_right, w=x, h=y),
            0, h, lambda x: 0, lambda x: w)[0]

        return result


# ----------------------------------------------------------------------------------------------------------------------


# Testing:
basis = {"phi_1": lambda x, y, w, h: (x + w) - (4 * y - h) + 1,
         "phi_2": lambda x, y, w, h: (2 * x - w) + (y + h) - 5,
         "d_phi_1": lambda x, y, w, h: 1,
         "d_phi_2": lambda x, y, w, h: 2
         }

_first = Node(2, 3)
_second = Node(2, 2)
_third = Node(3, 2)
_fourth = Node(3, 3)

rect = Rectangle(_first, _second, _third, _fourth, basis)

print(rect.mass(10, 10))
print(rect.stiffness(10, 10))
