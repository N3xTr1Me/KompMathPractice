from Interfaces.mesh.node_interface import INode

from Data.basis.basis import Basis

from typing import Tuple


# a node-dot on the 2D grid. Has (x,y) coordinates, a set of basis functions and nodal value, holds 2 neighboring
# node's coordinates
class Node(INode):
    def __init__(self, i: Tuple[float, float], j: Tuple[float, float], k: Tuple[float, float]):
        super(Node, self).__init__()

        # initializing node's coordinates and temperature
        self.__i = i

        # setting 2 neighbouring nodes
        self.__j = j
        self.__k = k

        # initializing node's basis functions, consisting of
        # the original function: ax + by + c,
        # and it's first derivative
        self.__basis = Basis(j, k)

        # Nodal value
        self.__u = None

    # ----------------------------------------------------------------------------------------------------------------------

    def x(self) -> float:
        return self.__i[0]

    def y(self) -> float:
        return self.__i[1]

    def coords(self) -> Tuple[float, float]:
        return self.__i

    # Returns "left" neighbours coordinates
    def j(self) -> Tuple[float, float]:
        return self.__j

    # Returns "right" neighbours coordinates
    def k(self) -> Tuple[float, float]:
        return self.__k

    # ------------------------------------------------------------------------------------------------------------------

    # Returns "a" constant from nodal basis function
    def a(self) -> float:
        return self.__basis.get_a()

    # Returns "b" constant from nodal basis function
    def b(self) -> float:
        return self.__basis.get_b()

    # Returns "c" constant from nodal basis function
    def c(self) -> float:
        return self.__basis.get_c()

    # ------------------------------------------------------------------------------------------------------------------

    # Returns nodal value
    def u(self) -> float:
        return self.__u

    # Sets nodal value
    def set_u(self, value: float) -> None:
        self.__u = value

    # Returns nodal basis function value from given arguments
    def phi(self, x: float, y: float) -> float:
        return self.__basis.phi()(x, y)

    # Returns nodal basis first derivative value from given arguments
    def d_phi(self, x: float, y: float) -> float:
        return self.__basis.d_phi()(x, y)

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
