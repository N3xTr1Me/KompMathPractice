

# a node-dot on the 2D grid. Has (x,y) coordinates and temperature
class Node:
    def __init__(self, x: float, y: float, t: float = None):
        self.__x = x
        self.__y = y

        self.__t = t

    def compact(self):
        return self.__x, self.__y, self.__t

    def x(self):
        return self.__x

    def y(self):
        return self.__y

    def get_t(self):
        return self.__t

    def set_t(self, value: float):
        self.__t = value

    def basis(self, x: float, y: float):
        if self.__x == x and self.__y == y:
            return self.__t
        else:
            return 0

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"({self.__x},{self.__y}): {self.__t}"

    def __eq__(self, other):

        xyt = self.compact()
        _xyt = other.compact()

        if xyt[0] == _xyt[0] and xyt[1] == _xyt[1]:
            return True

        return False

    def __add__(self, other):
        return self.__t + other.get_t()

    def __mul__(self, other):
        return self.__t * other.get_t()
