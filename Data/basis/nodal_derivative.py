from Data.basis.nodal_function import Phi

from typing import Dict


# First derivative of the nodal basis function
class DPhi(Phi):
    def __init__(self, constants: Dict[str, float], dx: bool = True):

        super(DPhi, self).__init__(constants)

        self._derivative = dx

    def _dx(self) -> bool:
        if self._derivative:
            return True

        return False

    def f(self) -> callable:
        return self(0, 0)

    def __call__(self, x: float, y: float):
        if self._dx():
            return self.a()

        return self.b()

    def __str__(self):
        return f"{self(0, 0)}"
