from Interfaces.grid.dot_interface import IDot

from typing import Tuple


class Dot(IDot):
    def __init__(self, x: float, y: float):
        self._x = x
        self._y = y

    def x(self) -> float:
        return self._x

    def y(self) -> float:
        return self._y

    def coords(self) -> Tuple[float, float]:
        return self.x(), self.y()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"{self._x, self._y}"

    def __eq__(self, other):
        if self.x() == other.x() and self.y() == other.y():
            return True
        return False
