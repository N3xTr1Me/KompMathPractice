import numpy as np
import random as rd

from Data.node import Node


max_temperature = 10


class M_matrix:
    def __init__(self, width: int, height: int):
        # self.matrix = np.zeroes(width-2, length-2)
        self.__width = width - 2
        self.__height = height - 2

        self.matrix = [[0 for _ in range(self.__width)] for _ in range(self.__height)]
        self.__center = [self.__width // 2, self.__height // 2]

        self.fill()

    def fill(self):
        global max_temperature

        for i in range(self.__height):
            for j in range(self.__width):
                if i == self.__center[1] and j == self.__center[0]:
                    self.matrix[i][j] = Node(j, i, max_temperature)
                    continue

                self.matrix[i][j] = Node(j, i, rd.randint(0, max_temperature))

mat = M_matrix(5, 4)
print(mat)
