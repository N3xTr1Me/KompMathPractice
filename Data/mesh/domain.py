import random
from typing import Tuple, List

import numpy as np

from Data.grid.Grid import Grid
from Data.mesh.node import Node
from Data.mesh.mesh import Mesh

from Data.matrices.mass_matrix import MassMatrix
from Data.matrices.stiffness_matrix import StiffnessMatrix

from Interfaces.mesh.domain_interface import IDomain


# A flyweight class, containing all the sessions defining the 2D region, which thermal conditions are to be found
class Domain:
    def __init__(self, dimensions: Tuple[int, int], heat_source: callable, steps: Tuple[int, int] = None,
                 nodes: List[Node] = None):

        # Setting domain area dimensions
        self.__width = dimensions[1]
        self.__height = dimensions[0]

        # Default x and y step on the grid
        if steps is None:
            steps = (1, 1)

        # Getting the target nodes on the mesh
        if nodes is not None:
            self.__nodes = nodes
        else:
            self.__nodes = self._generate_nodes(steps, heat_source)

        # Initializing grid
        self.__grid = Grid(self.x_interval(False), self.y_interval(False), steps, self.__nodes)

        # initializing mesh
        self.__mesh = Mesh(self.__grid, self.__nodes)

        # initializing nodal basis
        self.__basis = self.__mesh.get_basis(self.__nodes)

    def get_height(self) -> int:
        return self.__height

    def get_width(self) -> int:
        return self.__width

    def x_interval(self, for_nodes: bool = True) -> Tuple[int, int]:
        return 1 if for_nodes else 0, self.get_width()

    def y_interval(self, for_nodes: bool = True) -> Tuple[int, int]:
        return 1 if for_nodes else 0, self.get_height()

    def length(self) -> int:
        return len(self.__nodes)

    def _generate_nodes(self, steps: Tuple[int, int], f: callable) -> List[Node]:

        nodes = []

        y_int = self.y_interval()
        x_int = self.x_interval()

        for i in np.arange(y_int[0], y_int[1], steps[1]):
            for j in np.arange(x_int[0], x_int[1], steps[0]):
                nodes.append(Node(j, i, f(j, i)))

        return nodes

    # returns the load vector of the domains nodes
    def get_load(self, f: callable) -> np.array:
        load_vector = np.zeros((self.length(), 1))

        for i in range(self.length()):
            load_vector[i] = np.dot(f(self.__nodes[i].x(), self.__nodes[i].y()), self.__basis(i, self.__nodes[i]))

        return load_vector

    # Returns the mass matrix of the given finite element
    def mass_matrix(self) -> np.array:
        # size = self.length()
        # mass_matrix = np.zeros((size, size))
        #
        # for k in range(self.__mesh.k()):
        #     E = self.__mesh.get_mass(k)
        #
        #     for i in range(4):
        #         y = self.__mesh.get_y(k, i)
        #
        #         for j in range(4):
        #             x = self.__mesh.get_x(k, j)
        #
        #             mass_matrix[y][x] += E[i][j]
        #
        # return mass_matrix
        return MassMatrix(self.length(), self.__mesh).get_data()

    # Returns the stiffness matrix of the given finite element
    def stiffness_matrix(self) -> np.array:
        # size = self.length()
        # stiffness_matrix = np.zeros((size, size))
        #
        # for k in range(self.__mesh.k()):
        #     E = self.__mesh.get_stiffness(k)
        #
        #     for i in range(4):
        #         y = self.__mesh.get_y(k, i)
        #
        #         for j in range(4):
        #             x = self.__mesh.get_x(k, j)
        #
        #             stiffness_matrix[y][x] += E[i][j]
        #
        # return stiffness_matrix

        return StiffnessMatrix(self.length(), self.__mesh).get_data()

    # def update_u(self, ksi: np.array):
    #     for i in range(self.length()):
    #         self.__nodes[i].update(self.__basis(i, self.__nodes[i]) * ksi[i][0])


dom = Domain((5, 5), lambda x, y: random.randint(1, 10))
# mas = dom.mass_matrix()
# stiff = dom.stiffness_matrix()
print()
