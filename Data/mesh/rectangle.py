from Interfaces.mesh.finite_element import IFinite

from Data.grid.dot import Dot
from Data.basis.basis import Basis

from typing import Dict, List
import numpy as np


# A rectangular finite element on a 2D grid.
class Rectangle(IFinite):
    def __init__(self, nodes: List[List[Dot]]):
        super(Rectangle, self).__init__()

        # checking the minimal requirements
        if len(nodes) < 2 or len(nodes[0]) < 2 or len(nodes[1]) < 2:
            raise ValueError("Not enough dots to build a rectangle!")

        # checking if the form is correct
        if nodes[0][0].x() != nodes[1][0].x() or \
                nodes[1][0].y() != nodes[1][1].y() or \
                nodes[1][1].x() != nodes[0][1].x() or \
                nodes[0][1].y() != nodes[0][0].y():

            raise ValueError("Cannot build a rectangle with given nodes!")

        else:
            # initializing nodes
            self.__nodes = nodes

            # side length
            self.__h = self._get_h(nodes)

            # local basis of element
            self.__basis = Basis(self._constants(self.side()))

    # ------------------------------------------------------------------------------------------------------------------

    def _get_h(self, nodes: List[List[Dot]]) -> float:
        return 1

    def side(self) -> float:
        return self.__h

    def _constants(self, h: float) -> List[Dict[str, float]]:
        constants = []
        coefficient = 1 / h

        for i in range(4):
            constants.append(self._phi(i, coefficient))

        return constants

    def _phi(self, index: int, c: float) -> Dict[str, float]:
        if index == 0:
            return {"a": -1 * c, "b": -1 * c, "c": 1 * c}

        elif index == 1:
            return {"a": 1 * c, "b": 0, "c": 0}

        elif index == 2:
            return {"a": 0, "b": 1 * c, "c": 0}

        else:
            return {"a": 1 * c, "b": 1 * c, "c": 0}

    # ------------------------------------------------------------------------------------------------------------------

    def lower_left(self) -> Dot:
        return self.__nodes[0][0]

    def lower_right(self) -> Dot:
        return self.__nodes[0][1]

    def upper_left(self) -> Dot:
        return self.__nodes[1][0]

    def upper_right(self) -> Dot:
        return self.__nodes[1][1]

    # ------------------------------------------------------------------------------------------------------------------

    def _midpoint(self, start: Dot, end: Dot) -> Dot:
        return Dot(x=(end.x() + start.x()) / 2, y=(end.y() + start.y()) / 2)

    def _edge(self, i: int, j: int) -> Dot:
        if i == j:
            return self._midpoint(self.__nodes[i % 2][j % 2], self.__nodes[i % 2][j % 2])
        else:

            if i == 0:
                start = self.lower_left()

                if j == 1:
                    end = self.upper_left()

                elif j == 3:
                    end = self.lower_right()

                else:
                    return Dot(0, 0)

                return self._midpoint(start, end)

            elif i == 1:
                start = self.upper_left()

                if j == 0:
                    end = self.lower_left()

                elif j == 2:
                    end = self.upper_right()

                else:
                    return Dot(0, 0)

                return self._midpoint(start, end)

            elif i == 2:
                start = self.upper_right()

                if j == 1:
                    end = self.upper_left()

                elif j == 3:
                    end = self.lower_right()
                else:
                    return Dot(0, 0)

                return self._midpoint(start, end)

            else:
                start = self.lower_right()

                if j == 0:
                    end = self.lower_left()

                elif j == 2:
                    end = self.upper_right()
                else:
                    return Dot(0, 0)

                return self._midpoint(start, end)

    # Returns the local elemental mass matrix
    def mass(self) -> np.array:
        mass_matrix = np.zeros((4, 4), dtype=float)

        for i in range(4):
            for j in range(4):
                mass_matrix[i][j] = self.__basis(j, self._edge(i, j)) * \
                                    self.__basis(i, self._edge(i, j))

        return mass_matrix

    # Returns the local elemental stiffness matrix
    def stiffness(self) -> np.array:
        stiffness_matrix = np.zeros((4, 4), dtype=float)

        for i in range(4):
            for j in range(4):
                stiffness_matrix[i][j] = np.dot(self.__basis(j, self._edge(i, j), True),
                                                self.__basis(i, self._edge(i, j), True))

        return stiffness_matrix

    def __repr__(self):
        string = "|"

        for i in range(2):
            for j in range(2):
                string += str(self.__nodes[i][j])
        string += "|"

        return string

    # def area(self) -> float:
    #     return (self.upper_right().x() - self.lower_left().x()) * (self.upper_right().y() - self.lower_left().y())
    #
    # def form(self) -> Form:
    #     basis = dict()
    #
    #     for node in self.__nodes:
    #         basis[node] = self.__nodes[node].basis().get_nodal()
    #
    #     return Form(basis, self.area())
    #
    # def b_matrix(self) -> Matrix:
    #     rows, columns = 4, 4
    #
    #     vertexes = {0: "lower-left",
    #                 1: "upper-left",
    #                 2: "upper-right",
    #                 3: "lower-right"}
    #
    #     b = np.zeros((4, 4), dtype=float)
    #
    #     for i in range(rows):
    #         for j in range(columns):
    #             b[i][j] = self.__nodes[vertexes[i % 3]].b() * self.__nodes[vertexes[j % 3]].b()
    #
    #     return Matrix(rows, columns, b)
    #
    # def c_matrix(self) -> Matrix:
    #     rows, columns = 4, 4
    #
    #     vertexes = {0: "lower-left",
    #                 1: "upper-left",
    #                 2: "upper-right",
    #                 3: "lower-right"}
    #
    #     b = np.zeros((4, 4), dtype=float)
    #
    #     for i in range(rows):
    #         for j in range(columns):
    #             b[i][j] = self.__nodes[vertexes[i % 3]].c() * self.__nodes[vertexes[j % 3]].c()
    #
    #     return Matrix(rows, columns, b)

    # def k_1(self, x_conductivity, y_conductivity) -> Matrix:
    #     b = x_conductivity / (4 * self.area())
    #     c = y_conductivity / (4 * self.area())
    #
    #     return self.b_matrix() * b + self.c_matrix() * c
    #
    # def gradient(self) -> np.array:
    #     rows = 2
    #     columns = 4
    #
    #     gradient = np.zeros((rows, columns))
    #     i = 0
    #
    #     for node in self.__nodes:
    #         gradient[i][0] = self.__nodes[node].b()
    #         gradient[i][1] = self.__nodes[node].c()
    #
    #     return gradient

    # @staticmethod
    # def _property(x_conduct, y_conduct):
    #     prop = np.zeros((2, 2), dtype=float)
    #
    #     prop[0][0] = x_conduct
    #     prop[1][1] = y_conduct
    #
    #     return prop

# ll = Node((2, 2), 12)
# ul = Node((2, 3), -1)
# ur = Node((3, 3), 0)
# lr = Node((3, 2), 5)
#
# nodes = {"lower-left": ll,
#          "upper-left": ul,
#          "upper-right": ur,
#          "lower-right": lr}
#
# rect = Rectangle(nodes, lambda x, y: 1)
# print(rect.mass())
# print(rect.stiffness())
