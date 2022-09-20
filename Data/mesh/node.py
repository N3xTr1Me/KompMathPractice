from Data.basis.basis import Basis

from typing import Tuple


# a node-dot on the 2D grid. Has (x,y) coordinates and a set of basis functions, holds 2 neighboring node's coordinates
class Node:
    def __init__(self, i: Tuple[float, float], j: Tuple[float, float], k: Tuple[float, float]):
        super(Node, self).__init__()

        # initializing node's coordinates and temperature
        self.__i = i

        # setting 2 neighbouring nodes
        self.__j = j
        self.__k = k

        # initializing node's basis functions
        self.__basis = Basis(j, k)

    # ----------------------------------------------------------------------------------------------------------------------

    def x(self) -> float:
        return self.__i[0]

    def y(self) -> float:
        return self.__i[1]

    def coords(self) -> Tuple[float, float]:
        return self.__i

    def j(self) -> Tuple[float, float]:
        return self.__j

    def k(self) -> Tuple[float, float]:
        return self.__k

    # ------------------------------------------------------------------------------------------------------------------

    def basis(self) -> Basis:
        return self.__basis

    def a(self) -> float:
        return self.__basis.get_a()

    def b(self) -> float:
        return self.__basis.get_b()

    def c(self) -> float:
        return self.__basis.get_c()

    # ----------------------------------------------------------------------------------------------------------------------

    def __call__(self, *args, **kwargs):
        return self.__basis(*args, **kwargs)

    def __repr__(self):
        return f"|| {self.__j} - [" + self.__str__() + f"] - {self.__k} ||"

    def __str__(self):
        return f"{self.__i}"

    def __eq__(self, other):
        if self.x() == other.x() and self.y() == other.y():
            return True
        return False
