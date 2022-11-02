from typing import List, Tuple, Dict

import numpy as np

from Data.mesh.node import Node
from Data.grid.dot import Dot
from Data.grid.Grid import Grid
from Data.mesh.rectangle import Rectangle
from Data.basis.nodal.nodal_basis import Basis

from Interfaces.mesh.mesh_interface import IMesh


class Mesh:
    def __init__(self, grid: Grid, nodes: List[Node]):

        self.__grid = grid

        self.__quadrants = dict()

        self.__elements = self.map_mesh(nodes)

    # ------------------------------------------------------------------------------------------------------------------
    #                                        basic functionality
    # ------------------------------------------------------------------------------------------------------------------

    def width(self) -> int:
        return self.__grid.width()

    def height(self) -> int:
        return self.__grid.height()

    # def element(self, k: int) -> Rectangle:
    #     return self.__mesh[k]

    def get_elements(self) -> List[Rectangle]:
        return self.__elements

    # def get_mass(self, k: int) -> np.array:
    #     return self.__mesh[k].mass()
    #
    # def get_stiffness(self, k: int) -> np.array:
    #     return self.__mesh[k].stiffness()

    def get_x(self, element: int, index: int) -> float:
        return self.__elements[element][index].x()

    def get_y(self, element: int, index: int) -> float:
        return self.__elements[element][index].y()

    def k(self) -> int:
        if self.__elements is not None:
            return len(self.__elements)

        return 0

    def left_border(self, y_axis: bool = False) -> int:
        if y_axis:
            return self.__grid.left_border(y_axis) + self.__grid.y_step()

        return self.__grid.left_border() + self.__grid.x_step()

    def right_border(self, y_axis: bool = False) -> int:
        if y_axis:
            return self.__grid.right_border(y_axis)

        return self.__grid.right_border()

    def within(self, dot: Dot) -> bool:
        if self.left_border() < dot.x() < self.right_border() \
                and self.left_border(True) < dot.y() < self.right_border(True):
            return True

        return False

    def left_edge(self, dot: Dot, y_axis: bool = False) -> bool:
        if y_axis:
            return True if dot.y() == self.left_border(y_axis) else False

        return True if dot.x() == self.left_border() else False

    def right_edge(self, dot: Dot, y_axis: bool = False) -> bool:
        if y_axis:
            return True if dot.y() == self.right_border(y_axis) else False

        return True if dot.x() == self.right_border() else False

    # ------------------------------------------------------------------------------------------------------------------
    #                                      mesh mapping functionality
    # ------------------------------------------------------------------------------------------------------------------

    def _map_rects(self, dot: Dot) -> Dict[int, List[Dot]]:

        rects = dict()

        # Node is on the left border of the y interval
        if self.left_edge(dot, True):
            rects[3] = self.__grid.get_quadrant(dot.coords(), 3)

        # Node is on the left border of the x interval
        if self.left_edge(dot):
            rects[1] = self.__grid.get_quadrant(dot.coords(), 1)

        # Node is on the left borders of both x and y intervals
        if len(rects) >= 2:
            rects[0] = self.__grid.get_quadrant(dot.coords(), 0)

        # Node is on the right border of either x or y interval
        if self.right_edge(dot, True) or self.right_edge(dot):
            rects[2] = self.__grid.get_quadrant(dot.coords(), 2)

            return rects

        # Standard case
        rects[2] = self.__grid.get_quadrant(dot.coords(), 2)

        return rects

    # fills an element mesh around given nodes
    def map_mesh(self, nodes: List[Node]) -> List[Rectangle]:

        mesh = list()

        index = 0

        for i in range(len(nodes)):
            rects = self._map_rects(nodes[i])

            key = str(nodes[i])
            self.__quadrants[key] = dict()

            for rect in rects:
                self.__quadrants[key][rect] = index
                index += 1

                mesh.append(Rectangle(rects[rect]))

        return mesh

    # ------------------------------------------------------------------------------------------------------------------
    #                                      nodal basis functionality
    # ------------------------------------------------------------------------------------------------------------------

    def get_basis(self, nodes: List[Node]) -> Basis:
        constants = []

        for node in nodes:
            key = str(node)

            if key in self.__quadrants:
                constants.append(self._get_constant(node))
            else:
                raise ValueError(f"No elements containing {key}!")

        return Basis(constants)

    def _get_constant(self, node: Node, quadrant: int = 2) -> Dict[str, float | Node]:
        constants = dict()

        constants["k"] = self.__elements[self.__quadrants[str(node)][quadrant]][quadrant]
        constants["h_x"] = self.__elements[self.__quadrants[str(node)][quadrant]].side()
        constants["h_y"] = self.__elements[self.__quadrants[str(node)][quadrant]].side(True)

        return constants
