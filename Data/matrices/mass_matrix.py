from Data.matrices.matrix import Matrix
from Data.mesh.domain import Domain

import numpy as np


class MassMatrix(Matrix):
    def __init__(self, source: Domain, redefine: bool = False):

        rows, columns = source.rows(), source.columns()
        super(MassMatrix, self).__init__(rows=rows, columns=columns)

        self._source = source

        if not redefine:
            self._fill()

    def _get_from_src(self, row: int, index: int) -> np.array:
        return self._source.get_mass(row, index)

    def _fill(self):
        rows, columns = self._source.rows(), self._source.columns()
        matrix = None

        for i in range(rows):

            data = self._get_from_src(i, 0)
            row = Matrix(data.shape[0], data.shape[1], data)

            for j in range(1, columns):
                row.merge(self._get_from_src(i, j), axis=1)

            if i == 0:
                matrix = row

            else:
                matrix.merge(row.get_data())

        self._matrix = matrix.get_data()
        self._update_dimensions()
