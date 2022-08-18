from Data.rectangle import Rect


class Domain(Rect):
    def __init__(self, first, second, third, fourth):
        super().__init__(first, second, third, fourth)

    def check_domain(self, x: float, y: float):
        if self.__lower_left.x() < x < self.__upper_right.x() and self.__lower_left.y() < y < self.__upper_right.y():
            return self._temperature()

        return 0
    