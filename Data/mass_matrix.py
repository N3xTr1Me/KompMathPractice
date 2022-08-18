import random as rd
import numpy as np

from Data.node import Node
from Data.matrix_interface import Matrix

max_temperature = 10


class M_matrix(Matrix):
    def __init__(self, width: int, height: int):

        super(M_matrix, self).__init__()

        # self.matrix = np.zeroes(width-2, length-2)
        self.__width = width - 2
        self.__height = height - 2

        self.matrix = [[0 for _ in range(self.__width)] for _ in range(self.__height)]
        self.__center = [self.__width // 2, self.__height // 2]

        self.fill()

    def width(self):
        return self.__width

    def height(self):
        return self.__height

    def fill(self):
        global max_temperature

        for i in range(self.__height):
            for j in range(self.__width):
                if i == self.__center[1] and j == self.__center[0]:
                    self.matrix[i][j] = Node(j, i, max_temperature)
                    continue

                self.matrix[i][j] = Node(j, i, rd.randint(0, max_temperature))

    def add(self, other):

        result = M_matrix(self.__width + 2, self.__height + 2)

        for i in range(self.__height):
            for j in range(self.__width):
                result.matrix[i][j] = self.matrix[i][j] + other.matrix[i][j]

        return result

    def multiply(self, other):
        if self.__width == other.height():
            new_width = other.width() + 2
            new_height = self.height() + 2

            result = M_matrix(new_width, new_height)

            calc_self = [[0 for _ in range(self.width())] for _ in range(self.height())]
            calc_other = [[0 for _ in range(other.width())] for _ in range(other.height())]

            for i in range(self.__height):
                for j in range(self.__width):
                    calc_self[i][j] = self.matrix[i][j]

            for i in range(other.height()):
                for j in range(other.width()):
                    calc_other[i][j] = other.matrix[i][j]

            calc_result = np.multiply(np.array(calc_self), np.array(calc_other))

            for i in range(result.height()):
                for j in range(result.width()):
                    result.matrix[i][j] = Node(j, i, calc_result[i][j])

            return result

        else:
            raise ValueError(f"Invalid matrix dimensions. Cannot perform multiplication")


one = M_matrix(5, 5)
two = M_matrix(5, 5)
print(one.add(two).matrix)

print(one.multiply(two).matrix)
print()
