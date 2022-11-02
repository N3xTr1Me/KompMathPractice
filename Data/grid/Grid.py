from typing import Tuple, List

import numpy as np

from Data.grid.dot import Dot
from Data.mesh.node import Node


class Grid:
    def __init__(self, x_int: Tuple[int, int], y_int: Tuple[int, int],
                 steps: Tuple[int, int], nodes: List[Node] = None):

        self.__x = x_int
        self.__y = y_int

        self.__xstep = steps[0]
        self.__ystep = steps[1]

        self.__vertexes = []

        self.build_grid(nodes)

    def width(self) -> int:
        return self.__x[1] - self.__x[0] + 1

    def height(self) -> int:
        return self.__y[1] - self.__y[0] + 1

    def x_step(self) -> int:
        return self.__xstep

    def y_step(self) -> int:
        return self.__ystep

    def left_border(self, y_axis: bool = False) -> int:
        if y_axis:
            return self.__y[0]

        return self.__x[0]

    def right_border(self, y_axis: bool = False) -> int:
        if y_axis:
            return self.__y[1]

        return self.__x[1]

    def within_borders(self, coords: Tuple[int, int]):
        if self.__x[0] <= coords[0] <= self.__x[1] and self.__y[0] <= coords[1] <= self.__y[1]:
            return True

        return False

    def get_quadrant(self, coords: Tuple[int, int], quadrant: int) -> List[Dot]:

        if not self.within_borders(coords):
            raise ValueError(f"{coords} are out of the nodal range!")

        x, y = coords
        # lower-left quadrant
        # dot is in the upper-right position
        if quadrant == 0:
            return [
                self.__vertexes[y - self.y_step()][x - self.x_step()],
                self.__vertexes[y][x - self.x_step()],
                self.__vertexes[y][x],
                self.__vertexes[y - self.y_step()][x],
            ]

        # upper-left quadrant
        # dot is in the lower-right position
        if quadrant == 1:
            return [
                self.__vertexes[y][x - self.x_step()],
                self.__vertexes[y + self.y_step()][x - self.x_step()],
                self.__vertexes[y + self.y_step()][x],
                self.__vertexes[y][x],
            ]

        # upper-right quadrant
        # dot is in the lower-left position
        if quadrant == 2:
            return [
                self.__vertexes[y][x],
                self.__vertexes[y + self.y_step()][x],
                self.__vertexes[y + self.y_step()][x + self.x_step()],
                self.__vertexes[y][x + self.x_step()],
            ]

        # lower-right quadrant
        # dot is in the upper-left position
        if quadrant == 3:
            return [
                self.__vertexes[y - self.y_step()][x],
                self.__vertexes[y][x],
                self.__vertexes[y][x + self.x_step()],
                self.__vertexes[y - self.y_step()][x + self.x_step()],
            ]

        # Quadrant number is too big or too small
        raise ValueError(f"There is no quadrant numbered {quadrant}! (Only 4 quadrants exist on 2D grid)")

    # def set_nodes(self, nodes: List[Node]) -> None:
    #     self.__nodes = nodes
    #     self.__connections = self._set_connections()
    #
    # def create_nodes(self, x_step: float, y_step: float, f: callable):
    #     self.__nodes = self.generate_nodes(x_step, y_step, f)
    #     self.__connections = self._set_connections()

    def get_index(self, x: int, y: int, nodes: List[Node]) -> int:
        dot = Node(x, y, 0)
        try:
            return nodes.index(dot)
        except ValueError:
            return -1

    def build_grid(self, nodes: List[Node] = None) -> None:
        for i in range(0, self.height(), self.y_step()):
            self.__vertexes.append(list())

            for j in range(0, self.width(), self.x_step()):
                index = self.get_index(j, i, nodes)

                if 0 <= index < len(nodes):
                    self.__vertexes[i].append(nodes[index])

                else:
                    self.__vertexes[i].append(Dot(j, i))

    def __call__(self, index: int) -> List[Dot]:
        return self.__vertexes[index]

    # def _get_connections(self, index: int) -> List[Connection]:
    #
    #     # neighbours = {
    #     #     # rectangle in the lower-left corner
    #     #     0: {"by_x": -self.width(),
    #     #         "by_y": -1,
    #     #         "diag": -self.width() - 1},
    #     #
    #     #     # rectangle in the upper-left corner
    #     #     1: {"by_x": self.width(),
    #     #         "by_y": -1,
    #     #         "diag": self.width() - 1},
    #     #
    #     #     # rectangle in the upper-right corner
    #     #     2: {"by_x": self.width(),
    #     #         "by_y": 1,
    #     #         "diag": self.width() + 1},
    #     #     # rectangle in the lower-right corner
    #     #     3: {"by_x": -self.width(),
    #     #         "by_y": 1,
    #     #         "diag": -self.width() + 1},
    #     # }
    #
    #     quadrants = [0, 1, 2, 3]
    #     connections = []
    #
    #     for quadrant in quadrants:
    #         connections.append(Connection(index, quadrant, self.width(), self.node_exists))
    #
    #     return connections
    #
    # def _set_connections(self) -> List[List[Connection]]:
    #     connections = []
    #
    #     for i in range(len(self.__nodes)):
    #         connections.append(self._get_connections(i))
    #
    #     return connections
