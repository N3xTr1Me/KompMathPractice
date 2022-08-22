import random as rd
import numpy as np

from Data.node import Node
from Data.matrices.matrix import Matrix

from Data.field import Field

max_temperature = 10


class MassMatrix(Matrix):
    def __init__(self, rows: int, columns: int, field: Field):

        super(MassMatrix, self).__init__(rows=rows, columns=columns)

        # self.matrix = np.zeroes(width-2, length-2)
        self.__columns = super().columns()
        self.__rows = super().rows()

        self.matrix = [[0 for _ in range(self.__columns)] for _ in range(self.__rows)]
        self.__center = [self.__columns // 2, self.__rows // 2]

        self.fill(field)

    def fill(self, field: Field):
        self.matrix = field.grid()


one = MassMatrix(5, 5)
two = MassMatrix(5, 5)
print(one * two)

print()

print(one + two)
