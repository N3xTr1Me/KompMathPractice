from Interfaces.matrix.computation_interface import IComputable

from Data.matrices.matrix import Matrix
from Data.mesh.mesh import Mesh

import numpy as np


class MassMatrix(Matrix, IComputable):
    def __init__(self, size: int, source: callable, redefine: bool = False):
        super(MassMatrix, self).__init__(rows=size, columns=size)

        self.__source = source

        if not redefine:
            self._fill()

    def _get_from_src(self, k: int) -> np.array:
        return self.__source(k).mass()

    def _fill(self, elements: int):

        matrix = np.zeros((self.rows(), self.columns()))

        for k in range(elements):
            E = self._get_from_src(k)

            for i in range(4):
                y = source.get_y(k, i)

                for j in range(4):
                    x = source.get_x(k, j)

                    matrix[y][x] += E[i][j]

        self.update_data(matrix)
