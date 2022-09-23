import numpy as np

from Data.mesh.rectangle import Rectangle
from Data.grid.dot import Dot

from typing import List


class Cell:
    def __init__(self, element: Rectangle, connected=None):
        if connected is None:
            connected = []

        self.__element = element

        self.__neighbours = [connected]

    def freedom_degree(self) -> int:
        return len(self.__neighbours)

    def connections(self) -> List[int]:
        return self.__neighbours

    def h(self, y: bool = None) -> float:
        return self.__element.side(y)

    def get_mass(self) -> np.array:
        return self.__element.mass()

    def get_stiffness(self) -> np.array:
        return self.__element.stiffness()

    def get_element(self) -> Rectangle:
        return self.__element

    def __call__(self, x: int, y: int) -> Dot:
        return self.__element.get_dot(x, y)
