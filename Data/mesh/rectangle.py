from Interfaces.mesh.finite_element import IFinite

from Data.grid.dot import Dot
from Data.basis.elemental.elemental_basis import Elemental

from typing import Dict, List
import numpy as np


# A rectangular finite element on a 2D grid.
class Rectangle(IFinite):
    def __init__(self, nodes: List[Dot]):
        super(Rectangle, self).__init__()

        # checking the minimal requirements
        if len(nodes) < 4:
            raise ValueError("Not enough dots to build a rectangle!")

        # checking if the form is correct
        if nodes[0].x() != nodes[1].x() or \
                nodes[1].y() != nodes[2].y() or \
                nodes[2].x() != nodes[3].x() or \
                nodes[3].y() != nodes[0].y():

            raise ValueError("Cannot build a rectangle with given nodes!")

        else:
            # initializing nodes
            self.__nodes = nodes

            # side length
            self.__h = self._get_h(nodes)

            # elemental basis of element
            self.__basis = Elemental(self._constants())

    # ------------------------------------------------------------------------------------------------------------------

    def _check_dot(self, index: int, dot: Dot):
        if self.__nodes[index] == dot:
            return True

        return False

    def _get_h(self, nodes: List[Dot]) -> Dict[str, float]:
        return {"x": 1, "y": 1}

    def side(self, y: bool = False) -> float:
        if y:
            return self.__h["y"]

        return self.__h["x"]

    def _constants(self) -> List[Dict[str, float]]:
        constants = []

        for i in range(4):
            if i % 2 == 0:
                h = self.side(True)
            else:
                h = self.side()

            coefficient = 1 / h
            constants.append(self._phi(i, coefficient))

        return constants

    def _phi(self, index: int, c: float) -> Dict[str, float]:
        if index == 0:
            return {"a": -1 * c, "b": -1 * c, "c": 1 * c}

        elif index == 1:
            return {"a": 1 * c, "b": 0, "c": 0}

        elif index == 2:
            return {"a": 0, "b": 1 * c, "c": 0}

        else:
            return {"a": 1 * c, "b": 1 * c, "c": 0}

    # ------------------------------------------------------------------------------------------------------------------

    def lower_left(self) -> Dot:
        return self.__nodes[0]

    def lower_right(self) -> Dot:
        return self.__nodes[3]

    def upper_left(self) -> Dot:
        return self.__nodes[1]

    def upper_right(self) -> Dot:
        return self.__nodes[2]

    def diagonal(self, position: int) -> Dot:
        return self.__nodes[3 - position]

    def update_dot(self, index: int, dot: Dot):
        if self._check_dot(index, dot):
            self.__nodes[index] = dot
        else:
            raise ValueError(
                f"Given dot: {dot.coords()}, doesn't match {self.__nodes[y][x].coords()} it's trying to replace!")

    # ------------------------------------------------------------------------------------------------------------------

    def _midpoint(self, start: Dot, end: Dot) -> Dot:
        return Dot(x=(end.x() + start.x()) // 2, y=(end.y() + start.y()) // 2)

    def _edge(self, i: int, j: int) -> Dot:

        if i == j:
            return self.__nodes[i]

        if i % 2 != j % 2:
            return self._midpoint(self.__nodes[i], self.__nodes[j])

        return Dot(0, 0)

    # Returns the elemental mass matrix
    def mass(self) -> np.array:
        mass_matrix = np.zeros((4, 4), dtype=float)

        for i in range(4):
            for j in range(4):
                mass_matrix[i][j] = self.__basis(j, self._edge(i, j)) * \
                                    self.__basis(i, self._edge(i, j))

        return mass_matrix

    # Returns the elemental stiffness matrix
    def stiffness(self) -> np.array:
        stiffness_matrix = np.zeros((4, 4), dtype=float)

        for i in range(4):
            for j in range(4):
                stiffness_matrix[i][j] = np.dot(self.__basis(j, self._edge(i, j), True),
                                                self.__basis(i, self._edge(i, j), True))

        return stiffness_matrix

    def __getitem__(self, index: int) -> Dot:
        return self.__nodes[index]

    def __repr__(self):
        string = "|"

        for i in range(4):
            string += str(self.__nodes[i])

        string += "|"

        return string
