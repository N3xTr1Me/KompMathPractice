from typing import Tuple

from Data.basis.basis import Basis
from Data.right_side.functor import Functor
from Data.right_side.table import Table

from Model.algorithm.fem import FEM
from Model.file_handler.storage import Storage

from Model.algorithm.frame import Frame


class Model:
    def __init__(self, T: float, step: float, dimensions: Tuple[int, int], right_side: callable = None):

        # right border of I (time interval)
        self.__T = T
        # time step of I
        self.__t = step
        # current step
        self.__time_step = 0
        self.__step = 0

        # --------------------------------------------------------------------------------------------------------------

        cache_path = "./Cache/sessions/"
        config_path = "./Config/config.json"

        self.__storage = Storage(config_path, cache_path)
        self.__config = self.__storage.get_config()

        if right_side is None:
            self.__right_side = Table(dimensions[0], dimensions[1], self.__config["right-side"])
        else:
            self.__right_side = Functor(dimensions[0], dimensions[1], right_side)

        # --------------------------------------------------------------------------------------------------------------

        self.__basis = None

        self.__solver = FEM(dimensions, self.__right_side)

        self.__session = ""
        self.__cached = []

    def __current(self) -> Frame:
        return self.__storage.get_step(self.__session, self.__previous())

    def __previous(self) -> float:
        if self.__cached:
            return self.__cached[-1]
        else:
            return 0

    def __start_calculation(self):
        self.__session = self.__storage.start_session()

    def __cache(self, frame: Frame) -> None:
        self.__cached.append(self.__step)

        self.__storage.store(self.__session, self.__step, frame)

    def get(self, step: float) -> Frame:
        return self.__storage.get_step(self.__session, step)

    def make_step(self) -> Frame:

        if not self.__session:
            self.__start_calculation()

        if self.__time_step == 0:
            iteration = self.__solver.step(self.__t)
        else:
            iteration = self.__solver.step(self.__t, self.__current())

        self.__time_step = round(self.__time_step + self.__t, 7)
        self.__step += 1

        # iteration.set_temperatures(self.__basis)
        self.__cache(iteration)
        return iteration

    def run_algorithm(self) -> Frame:

        if not self.__session:
            self.__start_calculation()

        iteration = None

        while self.__time_step < self.__T:
            iteration = self.make_step()

        return iteration
