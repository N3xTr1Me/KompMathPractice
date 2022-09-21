from Data.right_side.boundary import Boundary

from typing import Dict


class Initial(Boundary):
    def __init__(self, width: int, height: int, condition: Dict[str, float]):
        self.__data = condition

        super(Initial, self).__init__(width, height, lambda x, y: self.__data[y][x])
