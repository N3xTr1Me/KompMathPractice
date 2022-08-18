from Data.node import Node


class Rect:
    def __init__(self, first: Node, second: Node, third: Node, fourth: Node):

        self.__lower_left = first
        self.__lower_right = fourth

        self.__upper_left = second
        self.__upper_right = third

    # basis function
    def check_domain(self, x: float, y: float):
        if self.__lower_left.x() < x < self.__upper_right.x() and self.__lower_left.y() < y < self.__upper_right.y():
            return self._temperature()

        return None

    # temperature approximation
    def _temperature(self):
        return sum((self.__lower_left.get_t(), self.__upper_left.get_t(),
                    self.__upper_right.get_t(), self.__lower_right.get_t())) / 4
