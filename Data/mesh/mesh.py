from typing import List, Tuple, Dict

import numpy as np

from Data.basis.nodal.nodal_basis import Basis
from Data.mesh.node import Node
from Data.grid.dot import Dot
from Data.mesh.rectangle import Rectangle

from Interfaces.mesh.mesh_interface import IMesh


class Mesh(IMesh):
    def __init__(self, x_int: Tuple[int, int], y_int: Tuple[int, int], x_step: float, y_step: float):

        self.__x = x_int
        self.__y = y_int

        self.__x_step = x_step
        self.__y_step = y_step

        self.__mesh = list()
        self.__connections = dict()

    # ------------------------------------------------------------------------------------------------------------------
    #                                        basic functionality
    # ------------------------------------------------------------------------------------------------------------------

    def width(self) -> int:
        return self.__x[1] - self.__x[0] + 1

    def height(self) -> int:
        return self.__y[1] - self.__y[0] + 1

    def x_step(self) -> float:
        return self.__x_step

    def y_step(self) -> float:
        return self.__y_step

    def get_mass(self, k: int) -> np.array:
        return self.__mesh[k].mass()

    def get_stiffness(self, k: int) -> np.array:
        return self.__mesh[k].stiffness()

    def get_x(self, element: int, index: int) -> float:
        return self.__mesh[element][index].x()

    def get_y(self, element: int, index: int) -> float:
        return self.__mesh[element][index].y()

    def k(self) -> int:
        if self.__mesh is not None:
            return len(self.__mesh)

        return 0

    def generate_nodes(self, f: callable) -> List[Node]:

        nodes = []

        for i in np.arange(self.__y[0], self.height() + self.__y_step, self.__y_step):
            for j in np.arange(self.__x[0], self.width() + self.__x_step, self.__x_step):
                nodes.append(Node(j, i, f(j, i)))

        return nodes

    # ------------------------------------------------------------------------------------------------------------------
    #                                      mesh mapping functionality
    # ------------------------------------------------------------------------------------------------------------------

    # checks if the given dot is withing the borders of the mesh
    def within_borders(self, dot: Dot) -> bool:
        if self.__x[0] < dot.x() < self.__x[1] and self.__y[0] < dot.y() < self.__y[1]:
            return True

        return False

    # checks if the dot is on the left border of either x or y intervals
    def _left_border(self, dot: Dot, y_axis: bool = False) -> bool:
        if y_axis:
            return True if dot.y() == self.__y[0] else False

        return True if dot.x() == self.__x[0] else False

    # checks if the dot is on the right border of either x or y intervals
    def _right_border(self, dot: Dot, y_axis: bool = False) -> bool:
        if y_axis:
            return True if dot.y() == self.__y[1] else False

        return True if dot.x() == self.__x[1] else False

    # checks if requested node is in the list of nodes
    def _node_exists(self, nodes: List[Node], index: int) -> bool:
        if index < len(nodes):
            return True

        return False

    # creates dot neighboring the given node
    def _make_dot(self, nodes: List[Node], index: int, position: int, target: int) -> Dot:
        # node is lower-left
        if position == 0:
            # target is lower-left
            if target == 0:
                return Dot(nodes[index].x(), nodes[index].y())

            # target is upper-left
            if target == 1:
                return Dot(nodes[index].x(), nodes[index].y() + self.y_step())

            # target is upper-right
            if target == 2:
                return Dot(nodes[index].x() + self.x_step(), nodes[index].y() + self.y_step())

            # target is lower-right
            if target == 3:
                return Dot(nodes[index].x() + self.x_step(), nodes[index].y())

            # target_pos if greater than 3
            raise ValueError(f"No target {target} in a rectangle!")

        # node is upper-left
        if position == 1:
            # target is lower-left
            if target == 0:
                return Dot(nodes[index].x(), nodes[index].y() - self.y_step())

            # target is upper-left
            if target == 1:
                return Dot(nodes[index].x(), nodes[index].y())

            # target is upper-right
            if target == 2:
                return Dot(nodes[index].x() + self.x_step(), nodes[index].y())

            # target is lower-right
            if target == 3:
                return Dot(nodes[index].x() + self.x_step(), nodes[index].y() - self.y_step())

            # target_pos if greater than 3
            raise ValueError(f"No target {target} in a rectangle!")

        # node is upper-right
        if position == 2:
            # target is lower-left
            if target == 0:
                return Dot(nodes[index].x() - self.x_step(), nodes[index].y() - self.y_step())

            # target is upper-left
            if target == 1:
                return Dot(nodes[index].x() - self.x_step(), nodes[index].y())

            # target is upper-right
            if target == 2:
                return Dot(nodes[index].x(), nodes[index].y())

            # target is lower-right
            if target == 3:
                return Dot(nodes[index].x(), nodes[index].y() - self.y_step())

            # target_pos if greater than 3
            raise ValueError(f"No target {target} in a rectangle!")

        if position == 3:
            # target is lower-left
            if target == 0:
                return Dot(nodes[index].x() - self.x_step(), nodes[index].y())

            # target is upper-left
            if target == 1:
                return Dot(nodes[index].x() - self.x_step(), nodes[index].y() + self.y_step())

            # target is upper-right
            if target == 2:
                return Dot(nodes[index].x(), nodes[index].y() + self.y_step())

            # target is lower-right
            if target == 3:
                return Dot(nodes[index].x(), nodes[index].y())

            # target_pos if greater than 3
            raise ValueError(f"No target {target} in a rectangle!")

        # position if greater than 3
        raise ValueError(f"No position {position} in a rectangle!")

    # returns node if it exists, if it doesn't, returns a newly created dot with needed coordinates instead
    def _get_node(self, nodes: List[Node], index: int, position: int, target_pos: int, shift: int = 0) -> Dot:
        if self._node_exists(nodes, index + shift) and index % self.width() != self.width() - 1:
            return nodes[index + shift]

        else:
            return self._make_dot(nodes, index, position, target_pos)

    # rectangle in lower-left section adjacent to node
    def _left_x(self, nodes: List[Node], index: int) -> List[Dot]:
        return [
            self._make_dot(nodes, index, 3, 0),
            self._make_dot(nodes, index, 3, 1),
            self._get_node(nodes, index, 3, 2, self.width()),
            nodes[index]  # node is lower-right
        ]

    # rectangle in lower-right section adjacent to node
    def _right_x(self, nodes: List[Node], index: int) -> List[Dot]:

        return [
            nodes[index],  # node is lower-left
            self._get_node(nodes, index, 0, 1, self.width()),
            self._make_dot(nodes, index, 0, 2),
            self._make_dot(nodes, index, 0, 3)
        ]

    # rectangle in upper-right section adjacent to node
    def _left_y(self, nodes: List[Node], index: int) -> List[Dot]:

        return [
            self._make_dot(nodes, index, 1, 0),
            nodes[index],  # node is upper-left
            self._get_node(nodes, index, 1, 2, 1),
            self._make_dot(nodes, index, 1, 3)
        ]

    # rectangle in lower-right section adjacent to node
    def _right_y(self, nodes: List[Node], index: int) -> List[Dot]:

        return [
            nodes[index],  # node is lower-left
            self._make_dot(nodes, index, 0, 1),
            self._make_dot(nodes, index, 0, 2),
            self._get_node(nodes, index, 0, 3, 1)
        ]

    # rectangle in upper-left section adjacent to node
    def _first_rect(self, nodes: List[Node], index: int) -> List[Dot]:

        return [
            self._make_dot(nodes, index, 2, 0),
            self._make_dot(nodes, index, 2, 1),
            nodes[index],  # node is upper-right
            self._make_dot(nodes, index, 2, 3)
        ]

    def _arrange_rect(self, nodes: List[Node], index: int) -> Dict[int, List[Dot]]:

        rects = dict()

        # in node is on the edges of determined area (lies on the lines determined by x and y interval border values)
        if not self.within_borders(nodes[index]):
            # if node is on the left border of x interval
            if self._left_border(nodes[index]):
                rects[1] = self._left_x(nodes, index)

            # if node is on the left border of y interval
            if self._left_border(nodes[index], True):
                rects[3] = self._left_y(nodes, index)

            # if node is on both x and y left borders
            if len(rects) >= 2:
                rects[0] = self._first_rect(nodes, index)

            # ----------------------------------------------------------------------------------------------------------

            # if node is on the right border of x interval
            if self._right_border(nodes[index]):
                rects[2] = self._right_x(nodes, index)

                return rects

            # if node is on the right border of y interval
            if self._right_border(nodes[index], True):
                rects[2] = self._right_y(nodes, index)

                return rects

        # standard case
        rects[2] = [nodes[index],
                    self._get_node(nodes, index, 0, 1, self.width()),
                    self._get_node(nodes, index, 0, 2, self.width() + 1),
                    self._get_node(nodes, index, 0, 3, 1),
                    ]

        return rects

    # fills an element mesh around given nodes
    def map_mesh(self, nodes: List[Node]) -> None:

        shift = 0

        for i in range(len(nodes)):

            rects = self._arrange_rect(nodes, i)
            self.__connections[str(nodes[i])] = {}

            for rect in rects:
                self.__connections[str(nodes[i])][rect] = shift
                self.__mesh.append(Rectangle(rects[rect]))
                shift += 1

    # ------------------------------------------------------------------------------------------------------------------
    #                                      nodal basis functionality
    # ------------------------------------------------------------------------------------------------------------------

    def basis(self, nodes: List[Node]) -> Basis:
        constants = []

        for node in nodes:
            key = str(node)
            if key in self.__connections:
                constants.append(self._constant(key))

        return Basis(constants)

    def _constant(self, node: str) -> Dict[str, float | Node]:
        constants = dict()

        constants["k"] = self._diagonal(node)
        constants["h_x"] = self.__mesh[self.__connections[node][2]].side()
        constants["h_y"] = self.__mesh[self.__connections[node][2]].side(True)

        return constants

    def _diagonal(self, node: str, rect: int = 2) -> Dot:
        rects = self.__connections[node]

        # node is upper-right
        if rect == 0:
            return self.__mesh[rects[rect]].lower_left()

        # node is lower-right
        if rect == 1:
            return self.__mesh[rects[rect]].upper_left()

        # node is lower-left
        if rect == 2:
            return self.__mesh[rects[rect]].upper_right()

        # node is upper-left
        return self.__mesh[rects[rect]].lower_right()
