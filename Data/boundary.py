from Interfaces.domain import IDomain
from Data.node import Node


class Boundary(IDomain):
    def __init__(self, lower_left: Node, upper_right: Node):
        super(Boundary, self).__init__()

        self.__lower_left = lower_left
        self.__upper_right = upper_right

    # checks if point with given coordinates is inside a rectangular domain area
    def within(self, x: float, y: float) -> bool:
        if self.__lower_left.x() <= x <= self.__upper_right.x() \
                and self.__lower_left.y() <= y <= self.__upper_right.y():

            return True

        return False
