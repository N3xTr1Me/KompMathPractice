from Interfaces.basis.functions.nodal_function import INodal

from Data.grid.dot import Dot


class Phi(INodal):
    def __init__(self, constants: dict):
        self._k = constants["k"]

        self._h = constants["h_x"] * constants["h_y"]

    def xk(self) -> float:
        return self._k.x()

    def yk(self) -> float:
        return self._k.y()

    def h(self) -> float:
        return self._h

    def f(self) -> callable:
        return lambda x, y: (self.xk() - x) * (self.yk() - y) / self._h

    def __call__(self, dot: Dot):
        return self.f()(dot.x(), dot.y())

    def __repr__(self):
        return f"({self.xk()} - x) * ({self.yk()} - y) / {self._h}"
