from Model.right_side.functor import Functor

from typing import List


class Table(Functor):
    def __init__(self, width: int, height: int, f: List[List[float]]):
        self.__data = f

        super(Table, self).__init__(width, height, lambda x, y: self.__data[y][x])


# tab = Table(4, 4, [[1, 1, 1, 1],
#                    [2, 2, 2, 2],
#                    [3, 3, 3, 3],
#                    [4, 4, 4, 4]])
# print(tab(-1, -1))
