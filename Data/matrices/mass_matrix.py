from Data.matrices.matrix import Matrix
from Data.mesh.domain import Domain

import numpy as np


class MassMatrix(Matrix):
    def __init__(self, source: Domain, redefine: bool = False):
        rows, columns = source.get_height(), source.get_width()
        super(MassMatrix, self).__init__(rows=rows, columns=columns)

        self._source = source

        if not redefine:
            self._fill()

    def _get_from_src(self) -> np.array:
        return self._source.get_mass()

    def _fill(self):
        self._matrix = self._get_from_src()
