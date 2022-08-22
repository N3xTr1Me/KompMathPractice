from Data.boundary import Boundary
from Data.node import Node
from Data.rectangle import Rectangle

from Interfaces.field_interface import IField

from typing import List, Dict, Tuple
import random


class Field(IField):
    def __init__(self, width: int, height: int, basis: Dict[str, callable],
                 heat_source: List[float] = None):
        self.__width = width
        self.__height = height

        self.__area = Boundary(Node(0, 0, basis), Node(self.__width - 1, self.__height - 1, basis))
        self.__heat_source = heat_source

        self.__grid = self._generate_nodes(basis)
        self.__mesh = self._map_mesh()

    def get_height(self) -> int:
        return self.__height

    def get_width(self) -> int:
        return self.__width

    # Returns the dimensions of the field
    def dimensions(self) -> Tuple[int, int]:
        return self.get_width(), self.get_height()

    def _rows(self) -> int:
        return self.get_height() - 3

    def _columns(self) -> int:
        return self.get_width() - 3

    # Returns the number of finite elements on the field.
    # The first digit is number of rows and second is the number of elements in each row
    def elements(self) -> Tuple[int, int]:
        return self._rows(), self._columns()

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
        n, m = self._rows(), self._columns()

        mesh = [[] for _ in range(n)]

        for i in range(0, n):
            for j in range(0, m):
                mesh[i].append(Rectangle(self.__grid[i + 1][j + 1], self.__grid[i + 2][j + 1],
                                         self.__grid[i + 2][j + 2], self.__grid[i + 1][j + 2]))

        return mesh

    # Returns the mass matrix of the given finite element
    def get_mass(self, row: int, index: int):
        return self.__mesh[row][index].mass(w=self.__width - 2, h=self.__height - 2)

    # Returns the stiffness matrix of the given finite element
    def get_stiffness(self, row: int, index: int):
        if self.__area.within(index, row):
            return self.__mesh[row][index].stiffness(w=self.__width - 2, h=self.__height - 2)
        return None
