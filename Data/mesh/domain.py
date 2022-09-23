import random
from typing import Dict, Tuple, List

import numpy as np

from Data.grid.dot import Dot
from Data.mesh.node import Node
from Data.mesh.rectangle import Rectangle
from Data.mesh.mesh import Mesh

from Interfaces.mesh.domain_interface import IDomain


# A flyweight class, containing all the sessions defining the 2D region, which thermal conditions are to be found
class Domain(IDomain):
    def __init__(self, dimensions: Tuple[int, int], heat_source: callable, nodes: List[Node] = None):

        self.__width = dimensions[1]
        self.__height = dimensions[0]

        if nodes is not None:
            self.__nodes = nodes
        else:
            self.__grid, self.__nodes = self._generate_nodes(heat_source)

        self.__mesh = Mesh(self.x_interval(), self.y_interval(), 1, 1)
        self.__mesh.map_mesh(self.__nodes)
        self.__basis = self.__mesh.basis(self.__nodes)

    def get_height(self) -> int:
        return self.__height

    def get_width(self) -> int:
        return self.__width

    def x_interval(self) -> Tuple[int, int]:
        return 1, self.get_width() - 1

    def y_interval(self) -> Tuple[int, int]:
        return 1, self.get_height() - 1

    def length(self) -> int:
        return len(self.__nodes)

    # Fills the grid on the field with nodes
    def _generate_nodes(self, heat_source: callable) -> Tuple[list, list]:
        height, width = self.get_height() - 1, self.get_width() - 1

        grid = [[Dot(x, y) for x in range(width)] for y in range(height)]

        nodes = []

        for i in range(height):
            for j in range(width):
                if 1 <= i < height and 1 <= j < width:
                    nodes.append(Node(j, i, heat_source(j, i)))

        return grid, nodes

    def get_load(self, f: callable) -> np.array:
        load_vector = np.zeros((self.length(), 1))

        for i in range(self.length()):
            load_vector[i] = np.dot(f(self.__nodes[i].x(), self.__nodes[i].y()), self.__basis(i, self.__nodes[i]))

        return load_vector

    # Returns the mass matrix of the given finite element
    def get_mass(self):
        rows, columns = self.length(), self.length()
        mass_matrix = np.zeros((rows, columns))

        for k in range(self.__mesh.k()):
            E = self.__mesh.get_element(k).mass()
            for i in range(4):
                print(i, end=" ")
                y = self.__mesh.get_y(k, i)
                for j in range(4):
                    print(j)
                    x = self.__mesh.get_x(k, j)
                    mass_matrix[y][x] += E[i][j]

        return mass_matrix

    # Returns the stiffness matrix of the given finite element
    def get_stiffness(self):
        rows, columns = self.get_height(), self.get_width()
        stiffness_matrix = np.zeros((rows, columns))

        for y in range(rows):
            for x in range(columns):
                stiffness_matrix[y][x] = self.__grid[y][x].i().d_phi(x, y) * self.__grid[y][x].j().d_phi(x, y)

        return stiffness_matrix

    def update_u(self, ksi: np.array):
        for i in range(self.length()):
            self.__nodes[i].update(self.__basis(i, self.__nodes[i]) * ksi[i][0])


dom = Domain((10, 10), lambda x, y: random.randint(1, 10))
mas = dom.get_mass()
print()
