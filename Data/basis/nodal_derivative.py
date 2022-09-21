import numpy as np

from Data.basis.nodal_function import Phi
from Data.grid.dot import Dot

from typing import Dict


# First derivative of the nodal basis function
class DPhi(Phi):
    def __init__(self, constants: Dict[str, float]):
        super(DPhi, self).__init__(constants)

    def f(self) -> callable:
        return lambda x, y: np.array([self.a(), self.b()])

    def __call__(self, dot: Dot):
        return self.f()(dot.x(), dot.y())

    def __str__(self):
        return f"{self.f()(0, 0)}"
