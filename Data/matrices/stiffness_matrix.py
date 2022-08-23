from Data.matrices.mass_matrix import MassMatrix
from Data.field import Field

import numpy as np


class StiffnessMatrix(MassMatrix):
    def __init__(self, source: Field):
        super(StiffnessMatrix, self).__init__(source=source, redefine=True)

        self.fill()

    def _get_from_src(self, row: int, index: int) -> np.array:
        return self._source.get_stiffness(row, index)
