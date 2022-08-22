from Interfaces.finite_element import IFinite
from Data.node import Node

import numpy
from scipy.integrate import dblquad


class Rectangle(IFinite):
    def __init__(self, first: Node, second: Node, third: Node, fourth: Node):
        super(Rectangle, self).__init__()

        # Rectangle vertexes are initialized clockwise starting from the lower_left
        self.__lower_left = first
        self.__lower_right = fourth

        self.__upper_left = second
        self.__upper_right = third

    # ----------------------------------------------------------------------------------------------------------------------

    # TODO: figure out a way to correctly integrate coordinate-dependent basis functions
    #  P.S. for now the basis functions are uniform for all of the nodes

    # returns the local mass matrix of the current finite element
    def mass(self, w: int, h: int) -> numpy.array:
        result = numpy.zeros((2, 2), dtype=float)

        result[0][0] = dblquad(
            lambda x, y: self.__upper_left.phi_1()(x, y) * self.__upper_left.phi_1()(x, y),
            0, h, lambda x: 0, lambda x: w)[0]

        result[0][1] = dblquad(
            lambda x, y: self.__upper_right.phi_1()(x, y) * self.__upper_right.phi_2()(x, y),
            0, h, lambda x: 0, lambda x: w)[0]

        result[1][0] = dblquad(
            lambda x, y: self.__lower_left.phi_2()(x, y) * self.__lower_left.phi_1()(x, y),
            0, h, lambda x: 0, lambda x: w)[0]

        result[1][1] = dblquad(
            lambda x, y: self.__lower_right.phi_2()(x, y) * self.__lower_right.phi_2()(x, y),
            0, h, lambda x: 0, lambda x: w)[0]
        return result

    # returns the local stiffness matrix of the current finite element
    def stiffness(self, w: int, h: int) -> numpy.array:
        result = numpy.zeros((2, 2), dtype=float)

        result[0][0] = dblquad(
            lambda x, y: self.__upper_left.d_phi_1()(x, y) * self.__upper_left.d_phi_1()(x, y),
            0, h, lambda x: 0, lambda x: w)[0]

        result[0][1] = dblquad(
            lambda x, y: self.__upper_right.d_phi_1()(x, y) * self.__upper_right.d_phi_2()(x, y),
            0, h, lambda x: 0, lambda x: w)[0]

        result[1][0] = dblquad(
            lambda x, y: self.__lower_left.d_phi_2()(x, y) * self.__lower_left.d_phi_1()(x, y),
            0, h, lambda x: 0, lambda x: w)[0]

        result[1][1] = dblquad(
            lambda x, y: self.__lower_right.d_phi_2()(x, y) * self.__lower_right.d_phi_2()(x, y),
            0, h, lambda x: 0, lambda x: w)[0]

        return result

# ----------------------------------------------------------------------------------------------------------------------

# # Testing:
# basis = {"phi_1": lambda x, y: (3 * x) - y + 6,
#          "phi_2": lambda x, y: (2 * x) + (5 * y) - 7,
#          "d_phi_1": lambda x, y: 3,
#          "d_phi_2": lambda x, y: 2
#          }
#
# first = Node(1, 1, basis)
# second = Node(1, 12, basis)
# third = Node(10, 12, basis)
# fourth = Node(10, 1, basis)
#
# rect = Rectangle(first, second, third, fourth)
#
# print(rect.mass(4, 5))
# print(rect.stiffness(4, 5))
