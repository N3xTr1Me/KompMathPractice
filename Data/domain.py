from Data.border import Border
from Data.node import Node
from Data.rectangle import Rectangle

from Interfaces.domain_interface import IDomain

from typing import List, Dict
import random


# A flyweight class, containing all the data defining the 2D region, which thermal conditions are to be found
class Domain(IDomain):
    def __init__(self, width: int, height: int, basis: Dict[str, callable],
                 heat_source: List[float] = None):

        # Initial field dimensions
        self.__width = width
        self.__height = height

        # Field border and thermal source
        self.__area = Border(Node(0, 0, basis), Node(self.get_width() - 1, self.get_height() - 1, basis))
        self.__heat_source = heat_source

        # Table of nodes on the field
        self.__grid = self._generate_nodes(basis)
        # Table of finite elements, built on the field nodes
        self.__mesh = self._map_mesh()

    def get_height(self) -> int:
        return self.__height

    def get_width(self) -> int:
        return self.__width

    # returns the number of rows of the mesh table
    def rows(self) -> int:
        return self.get_height() - 3

    # returns the number of columns of the mesh table
    def columns(self) -> int:
        return self.get_width() - 3

    # Fills the field with nodes
    def _generate_nodes(self, basis: Dict[str, callable]) -> list:
        n, m = self.get_height(), self.get_width()

        grid = [[None for _ in range(m)] for _ in range(n)]

        for i in range(n):
            for j in range(m):
                if self.__area.within(j, i):
                    t = random.randint(1, 10)
                else:
                    t = 0

                grid[i][j] = Node(j, i, basis, t)

        return grid

    # Constructs the rectangular finite elements from the nodes on the field
    def _map_mesh(self) -> list:
        rows, columns = self.rows(), self.columns()

        mesh = [[] for _ in range(rows)]

        for i in range(0, rows):
            for j in range(0, columns):
                mesh[i].append(Rectangle(self.__grid[i + 1][j + 1], self.__grid[i + 2][j + 1],
                                         self.__grid[i + 2][j + 2], self.__grid[i + 1][j + 2]))

        return mesh

    # Returns the mass matrix of the given finite element
    def get_mass(self, row: int, column: int):
        return self.__mesh[row][column].mass(w=self.__width - 2, h=self.__height - 2)

    # Returns the stiffness matrix of the given finite element
    def get_stiffness(self, row: int, column: int):
        return self.__mesh[row][column].stiffness(w=self.__width - 2, h=self.__height - 2)
