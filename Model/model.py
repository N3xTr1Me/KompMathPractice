from typing import Tuple

from Data.basis import Basis
from Model.fem import FEM

from Model.frame import Frame


class Model:
    def __init__(self, T: int, step: float, dimensions: Tuple[int, int], right_side: callable):

        self.__basis = Basis({"phi_1": lambda x, y, w, h: (x + w) - (4 * y - h) + 1,
                              "phi_2": lambda x, y, w, h: (2 * x - w) + (y + h) - 5,
                              "d_phi_1": lambda x, y, w, h: 1,
                              "d_phi_2": lambda x, y, w, h: 2
                              })

        self.__T = T
        self.__step = step

        self.__solver = FEM(dimensions, self.__basis, right_side)

        self.__cache = []

        self.__solution = {"dimensions": dimensions,
                           "basis": self.__basis,
                           "coefficients": None
                           }

    def __current(self):
        return self.__cache[-1]

    def __previous(self):
        return self.__cache[-2]

    def __cache(self, value: Frame):
        self.__cache.append(value)
