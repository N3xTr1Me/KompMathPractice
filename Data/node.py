from typing import Dict

from Interfaces.basis import IBasis


# a node-dot on the 2D grid. Has (x,y) coordinates and temperature
class Node(IBasis):
    def __init__(self, x: float, y: float, basis_funcs: Dict[callable], t: float = None):
        super(Node, self).__init__()

        # initializing node's coordinates and temperature
        self.__x = x
        self.__y = y
        self.__t = t

        # checking the minimal basis requirements
        if "phi_1" not in basis_funcs:
            raise ValueError("phi_1 not found in basis!")
        elif "phi_2" not in basis_funcs:
            raise ValueError("phi_2 not found in basis!")
        elif "d_phi_1" not in basis_funcs:
            raise ValueError("d_phi_1 not found in basis!")
        elif "d_phi_2" not in basis_funcs:
            raise ValueError("d_phi_2 not found in basis!")

        # initializing node's basis
        self.__basis = dict()
        for func in basis_funcs:
            self.__basis[func] = basis_funcs[func]

# ----------------------------------------------------------------------------------------------------------------------

    def x(self) -> float:
        return self.__x

    def y(self) -> float:
        return self.__y

    def get_t(self) -> float:
        return self.__t

    def set_t(self, value: float) -> None:
        self.__t = value

# ----------------------------------------------------------------------------------------------------------------------
    # first basis function for node
    def phi_1(self) -> callable:
        return self.basis("phi_1")

    # second basis function for node
    def phi_2(self) -> callable:
        return self.basis("phi_2")

    # first derivative of the first basis function for node
    def d_phi_1(self) -> callable:
        return self.basis("d_phi_1")

    # first derivative of the second basis function for node
    def d_phi_2(self) -> callable:
        return self.basis("d_phi_2")

    # getter method for basis functions
    def basis(self, function):
        if function in self.__basis:
            return self.__basis[function]
        raise KeyError(f"{function} not found among basis functions!")

# ----------------------------------------------------------------------------------------------------------------------

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"({self.__x},{self.__y}): {self.__t}"

    def __eq__(self, other):

        if self.__x == other.x() and self.__y == other.y():
            return True

        return False
