from typing import Tuple

from Data.basis import Basis
from Model.fem import FEM
from Model.file_handler import Storage

from Model.frame import Frame


class Model:
    def __init__(self, T: int, step: float, dimensions: Tuple[int, int], right_side: callable):
        self.__T = T
        self.__t = step
        self.__step = 0

        # --------------------------------------------------------------------------------------------------------------

        self.__basis = Basis({"phi_1": lambda x, y, w, h: (x + w) - (4 * y - h) + 1,
                              "phi_2": lambda x, y, w, h: (2 * x - w) + (y + h) - 5,
                              "d_phi_1": lambda x, y, w, h: 1,
                              "d_phi_2": lambda x, y, w, h: 2
                              })

        self.__solver = FEM(dimensions, self.__basis, right_side)

        # --------------------------------------------------------------------------------------------------------------

        cache_path = "../Cache/data/"
        config_path = "../Config/config.json"

        self.__storage = Storage(config_path, cache_path)
        self.__config = self.__storage.get_config()

        self.__session = ""
        self.__cached = []

    def __current(self) -> Frame:
        return self.__storage.get_step(self.__session, self.__cache[-1])

    def __previous(self) -> Frame:
        return self.__storage.get_step(self.__session, self.__cache[-2])

    def __cache(self, step: Frame) -> None:
        self.__cached.append(step.t())

        self.__storage.store(self.__session, step)

    def get(self, step: float) -> Frame:
        return self.__storage.get_step(self.__session, step)

    def make_step(self) -> Frame:
        iteration = self.__solver.step(self.__t, self.__current(), self.__previous())

        self.__step += self.__t

        iteration.set_temperatures(self.__basis)
        self.__cache(iteration)
        return iteration

