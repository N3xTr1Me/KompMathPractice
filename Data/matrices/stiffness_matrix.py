from Data.matrices.mass_matrix import MassMatrix

import numpy as np

from Data.mesh.mesh import Mesh


class StiffnessMatrix(MassMatrix):
    def __init__(self, size: int, source: Mesh):
        super(StiffnessMatrix, self).__init__(size=size, source=source, redefine=True)

        self._fill(source)

    def _get_from_src(self, source: Mesh, k: int) -> np.array:
        return source.get_stiffness(k)
