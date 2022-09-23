from Interfaces.model.right_side import IRightSide

from Data.grid.dot import Dot


class Boundary(IRightSide):
    def __init__(self, width: int, height: int, f: callable):

        self._width = width
        self._height = height

        self._f = f

    def within(self, dot: Dot) -> bool:
        if (0 < dot.x() <= self._width - 1) and (0 < dot.y() <= self._height - 1):
            return True
        return False

    def __call__(self, dot: Dot) -> float:
        if self.within(dot):
            return self._f(x=dot.x(), y=dot.y())

        return 0
