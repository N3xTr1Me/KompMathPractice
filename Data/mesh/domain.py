from Data.basis.basis import Basis
from Data.mesh.node import Node
from Data.mesh.rectangle import Rectangle

from Interfaces.mesh.domain_interface import IDomain


# A flyweight class, containing all the sessions defining the 2D region, which thermal conditions are to be found
class Domain(IDomain):
    def __init__(self, width: int, height: int, basis: Basis,
                 heat_source: callable):

        # Initial mesh dimensions
        self.__width = width
        self.__height = height

        # Table of nodes on the mesh
        self.__grid = self._generate_nodes(heat_source)
        # Table of finite elements, built on the mesh nodes
        self.__mesh = self._map_mesh(basis)

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

    # Fills the grid on the field with nodes
    def _generate_nodes(self, heat_source: callable) -> list:
        n, m = self.get_height(), self.get_width()

        grid = [[None for _ in range(m)] for _ in range(n)]

        for i in range(n):
            for j in range(m):
                t = heat_source(j, i)

                grid[i][j] = Node(j, i, t)

        return grid

    # Constructs the rectangular finite elements from the nodes to form mesh
    def _map_mesh(self, basis: Basis) -> list:
        rows, columns = self.rows(), self.columns()

        mesh = [[] for _ in range(rows)]

        for i in range(0, rows):
            for j in range(0, columns):
                mesh[i].append(Rectangle(self.__grid[i + 1][j + 1], self.__grid[i + 2][j + 1],
                                         self.__grid[i + 2][j + 2], self.__grid[i + 1][j + 2], basis))

        return mesh

    # Returns the mass matrix of the given finite element
    def get_mass(self, row: int, column: int):
        return self.__mesh[row][column].mass(w=self.__width - 2, h=self.__height - 2)

    # Returns the stiffness matrix of the given finite element
    def get_stiffness(self, row: int, column: int):
        return self.__mesh[row][column].stiffness(w=self.__width - 2, h=self.__height - 2)

    def update_t(self, row: int, column: int, value: float):
        self.__grid[row][column].set_t(value)
