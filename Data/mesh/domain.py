from typing import Dict, Tuple

import numpy as np

from Data.grid.dot import Dot
from Data.mesh.node import Node
from Data.mesh.rectangle import Rectangle

from Interfaces.mesh.domain_interface import IDomain


# A flyweight class, containing all the sessions defining the 2D region, which thermal conditions are to be found
class Domain(IDomain):
    def __init__(self, width: int, height: int, heat_source: callable):

        # Initial mesh dimensions
        self.__width = width
        self.__height = height

        # Table of nodes on the mesh
        self.__grid = self._generate_nodes()
        # Table of finite elements, built on the mesh nodes
        self.__mesh = self._map_mesh(heat_source)

    def get_height(self) -> int:
        return self.__height

    def get_width(self) -> int:
        return self.__width

    # returns the number of rows of the mesh table
    def rows(self) -> int:
        return self.get_height() * 2

    # returns the number of columns of the mesh table
    def columns(self) -> int:
        return self.get_width() * 2

    def _arrange_rect(self, x: float, y: float) -> Dict[str, Node]:
        nodes = dict()

        nodes["lower-left"] = self.__grid[y][x]
        nodes["upper-left"] = self.__grid[y + 1][x]
        nodes["upper-right"] = self.__grid[y + 1][x + 1]
        nodes["lower-right"] = self.__grid[y][x + 1]

        return nodes

    # Fills the grid on the field with nodes
    def _generate_nodes(self) -> Tuple[list, list]:
        height, width = self.get_height(), self.get_width()

        grid = [[Dot(x, y) for x in range(width)] for y in range(height)]

        nodes = []

        for i in range(height):
            for j in range(width):
                if i % 2 == 1 and j % 2 == 1:
                    nodes.append(Node(j, i, 0))

        for i in range(width):
            if i % 2 == 1:
                nodes.append(Node(i, height - 1, 0))

        for i in range(height):
            if i % 2 == 1:
                nodes.append(Node(width - 1, i, 0))

        return grid, nodes

    # Constructs the rectangular finite elements from the nodes to form mesh
    def _map_mesh(self, heat_source: callable) -> list:
        rows, columns = self.get_height() - 1, self.get_width() - 1

        mesh = [[] for _ in range(rows)]

        for i in range(0, rows):
            for j in range(0, columns):
                nodes = self._arrange_rect(j, i)
                mesh[i].append(Rectangle(nodes, heat_source))

        return mesh

    # Returns the mass matrix of the given finite element
    def get_mass(self):
        rows, columns = self.get_height(), self.get_width()
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

    def update_u(self, row: int, column: int, value: float):
        self.__grid[row][column].set_u(value)
