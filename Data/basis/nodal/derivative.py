import numpy as np

from Data.basis.nodal.function import Phi


class DPhi(Phi):
    def __init__(self, constants: dict):
        super(DPhi, self).__init__(constants)

    def dx(self, y: float) -> float:
        return (y - self._k.y()) / self._h

    def dy(self, x: float) -> float:
        return (x - self._k.x()) / self._h

    def f(self) -> callable:
        return lambda x, y: np.array([self.dy(x), self.dx(y)])

    def __repr__(self):
        return f"[(y - {self._k.y()}) / {self._h}, (x - {self._k.x()}) / {self._h}]"
