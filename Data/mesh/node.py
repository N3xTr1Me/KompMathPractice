

# a node-dot on the 2D grid. Has (x,y) coordinates and temperature
class Node:
    def __init__(self, x: float, y: float, t: float = None):
        super(Node, self).__init__()

        # initializing node's coordinates and temperature
        self.__x = x
        self.__y = y
        self.__t = t

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

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"({self.__x},{self.__y}): {self.__t}"

    def __eq__(self, other):
        if self.__x == other.x() and self.__y == other.y():
            return True
        return False
