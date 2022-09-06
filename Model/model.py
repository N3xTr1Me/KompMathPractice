import random
from typing import Tuple

from Data.basis import Basis
from Model.right_side.functor import Functor
from Model.right_side.table import Table

from Model.fem import FEM
from Model.file_handler import Storage

from Model.frame import Frame

import datetime


class Model:
    def __init__(self, T: int, step: float, dimensions: Tuple[int, int], right_side: callable = None):

        # right border of I (time interval)
        self.__T = T
        # time step of I
        self.__t = step
        # current step
        self.__step = 0

        # --------------------------------------------------------------------------------------------------------------

        cache_path = "../Cache/data/"
        config_path = "../Config/config.json"

        self.__storage = Storage(config_path, cache_path)
        self.__config = self.__storage.get_config()

        if right_side is None:
            self.__right_side = Table(dimensions[0], dimensions[1], self.__config["right-side"])
        else:
            self.__right_side = Functor(dimensions[0], dimensions[1], right_side)

        # --------------------------------------------------------------------------------------------------------------

        self.__basis = Basis({"phi_1": lambda x, y, w, h: (x + w) - (4 * y - h) + 1,
                              "phi_2": lambda x, y, w, h: (2 * x - w) + (y + h) - 5,
                              "d_phi_1": lambda x, y, w, h: 1,
                              "d_phi_2": lambda x, y, w, h: 2
                              })

        self.__solver = FEM(dimensions, self.__basis, self.__right_side)

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

    def __cache(self, step: Frame) -> None:
        self.__cached.append(step.t())

        self.__storage.store(self.__session, step)

    def get(self, step: float) -> Frame:
        return self.__storage.get_step(self.__session, step)

    def make_step(self) -> Frame:

        if not self.__session:
            self.__start_calculation()

        if self.__step == 0:
            iteration = self.__solver.step(self.__t)
        else:
            iteration = self.__solver.step(self.__t, self.__current())

        self.__step += self.__t

        iteration.set_temperatures(self.__basis)
        self.__cache(iteration)
        return iteration

    def run_algorithm(self):

        if not self.__session:
            self.__start_calculation()

        while self.__step < self.__T:
            iteration = self.make_step()


dims = (10, 10)
time = 10
time_step = 1

start_1 = datetime.datetime.now()
model = Model(T=time, step=time_step, dimensions=dims, right_side=lambda x, y: random.randint(1, 10))

start_2 = datetime.datetime.now()
model.run_algorithm()
print(datetime.datetime.now() - start_2)
print(datetime.datetime.now() - start_1)
