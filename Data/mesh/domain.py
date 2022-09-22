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

        if nodes is not None:
            self.__nodes = nodes
        else:
            self.__grid, self.__nodes = self._generate_nodes(heat_source)

        self.__mesh = Mesh(dimensions[0], dimensions[1], self.__nodes)
        self.__basis = self.__mesh.basis(self.__nodes)

    def get_height(self) -> int:
        return self.__mesh.height()

    def get_width(self) -> int:
        return self.__mesh.width()

    def length(self) -> int:
        return len(self.__nodes)

    # Fills the grid on the field with nodes
    def _generate_nodes(self, heat_source: callable) -> Tuple[list, list]:
        height, width = self.get_height(), self.get_width()

        grid = [[Dot(x, y) for x in range(width)] for y in range(height)]

        nodes = []

        for i in range(height):
            for j in range(width):
                if i % 2 == 1 and j % 2 == 1:
                    nodes.append(Node(j, i, heat_source(j, i)))

        for i in range(width):
            if i % 2 == 1:
                nodes.append(Node(i, height - 1, heat_source(j, i)))

        for i in range(height):
            if i % 2 == 1:
                nodes.append(Node(width - 1, i, heat_source(j, i)))

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

        for y in range(rows):
            for x in range(columns):
                mass_matrix[y][x] = self.__grid[y][x].i().phi(x, y) * self.__grid[y][x].j().phi(x, y)

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
