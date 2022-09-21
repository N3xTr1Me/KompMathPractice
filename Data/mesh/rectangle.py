from Interfaces.mesh.finite_element import IFinite

from Data.mesh.node import Node

from typing import Dict
import numpy as np


# A rectangular finite element on a 2D grid.
class Rectangle(IFinite):
    def __init__(self, nodes: Dict[str, Node], f: callable):
        super(Rectangle, self).__init__()

        # checking the minimal requirements
        vertexes = ["lower-left", "upper-left", "upper-right", "lower-right"]

        for vertex in vertexes:
            if vertex not in nodes:
                raise ValueError(f"{vertex} not found among nodes!")

        # checking if the form is correct
        if nodes["lower-left"].x() != nodes["upper-left"].x() or \
                nodes["upper-left"].y() != nodes["upper-right"].y() or \
                nodes["upper-right"].x() != nodes["lower-right"].x() or \
                nodes["lower-right"].y() != nodes["lower-left"].y():

            raise ValueError("Cannot build a rectangle with given nodes!")

        else:
            # initializing nodes
            self.__nodes = self._set_connections(nodes)

            # initializing nodal values
            self._set_values(f)

    # ------------------------------------------------------------------------------------------------------------------

    def _set_connections(self, nodes: Dict[str, Node]) -> Dict[str, Node]:
        nodes["lower-left"].set_neighbours(nodes["lower-right"], nodes["upper-left"])
        nodes["upper-left"].set_neighbours(nodes["lower-left"], nodes["upper-right"])
        nodes["upper-right"].set_neighbours(nodes["upper-left"], nodes["lower-right"])
        nodes["lower-right"].set_neighbours(nodes["upper-right"], nodes["lower-left"])

        return nodes

    # Sets nodal values for nodes
    def _set_values(self, f: callable) -> None:

        for node in self.__nodes:
            x, y = self.__nodes[node].coords()
            self.__nodes[node].set_u(f(x, y))

    # ------------------------------------------------------------------------------------------------------------------

    def lower_left(self) -> Node:
        return self.__nodes["lower-left"]

    def lower_right(self) -> Node:
        return self.__nodes["lower-right"]

    def upper_left(self) -> Node:
        return self.__nodes["upper-left"]

    def upper_right(self) -> Node:
        return self.__nodes["upper-right"]

    # ------------------------------------------------------------------------------------------------------------------

    # Returns the local elemental mass matrix
    def mass(self) -> np.array:
        mass_matrix = np.zeros((2, 2), dtype=float)

        x, y = self.lower_left().coords()
        mass_matrix[0][0] = self.lower_right().phi(x, y) * self.upper_left().phi(x, y)

        x, y = self.upper_left().coords()
        mass_matrix[0][1] = self.lower_left().phi(x, y) * self.upper_right().phi(x, y)

        x, y = self.upper_right().coords()
        mass_matrix[1][1] = self.upper_left().phi(x, y) * self.lower_right().phi(x, y)

        x, y = self.lower_right().coords()
        mass_matrix[1][0] = self.upper_right().phi(x, y) * self.lower_left().phi(x, y)

        return mass_matrix

    # Returns the local elemental stiffness matrix
    def stiffness(self) -> np.array:
        stiffness_matrix = np.zeros((2, 2), dtype=float)

        x, y = self.lower_left().coords()
        stiffness_matrix[0][0] = self.lower_right().d_phi(x, y) * self.upper_left().d_phi(x, y)

        x, y = self.upper_left().coords()
        stiffness_matrix[0][1] = self.lower_left().d_phi(x, y) * self.upper_right().d_phi(x, y)

        x, y = self.upper_right().coords()
        stiffness_matrix[1][1] = self.upper_left().d_phi(x, y) * self.lower_right().d_phi(x, y)

        x, y = self.lower_right().coords()
        stiffness_matrix[1][0] = self.upper_right().d_phi(x, y) * self.lower_left().d_phi(x, y)

        return stiffness_matrix

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
# rect = Rectangle(nodes, lambda x, y: random.randint(1, 10))
# print(rect.mass())
# print(rect.stiffness())
