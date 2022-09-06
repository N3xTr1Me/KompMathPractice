from Interfaces.right_side import IRightSide


class Functor(IRightSide):
    def __init__(self, width: int, height: int, f: callable):

        self._width = width
        self._height = height

        self._f = f

    def within(self, x: float, y: float) -> bool:
        if (0 <= x <= self._width - 1) and (0 <= y <= self._height - 1):
            return True
        return False

    def __call__(self, x: float, y: float) -> float:
        if self.within(x, y):
            return self._f(x=x, y=y)

        return 0
