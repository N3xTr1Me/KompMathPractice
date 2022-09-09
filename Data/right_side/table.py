from Data.right_side.functor import Functor

from typing import List


class Table(Functor):
    def __init__(self, width: int, height: int, f: List[List[float]]):
        self.__data = f

        super(Table, self).__init__(width, height, lambda x, y: self.__data[y][x])
