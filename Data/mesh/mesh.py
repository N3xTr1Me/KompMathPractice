from typing import List, Tuple

from Data.basis.basis import Basis
from Data.mesh.node import Node
from Data.grid.dot import Dot
from Data.mesh.rectangle import Rectangle


class Mesh:
    def __init__(self, x_int: Tuple[int, int], y_int: Tuple[int, int], x_step: float, y_step: float):

        self.__x = x_int
        self.__y = y_int

        self.__x_step = x_step
        self.__y_step = y_step

        self.__mesh = []

    def width(self) -> int:
        return self.__x[1] - self.__x[0] + 1

    def height(self) -> int:
        return self.__y[1] - self.__y[0] + 1

    def x_step(self) -> float:
        return self.__x_step

    def y_step(self) -> float:
        return self.__y_step

    def get_element(self, k: int):
        return self.__mesh[k]

    def k(self) -> int:
        if self.__mesh is not None:
            return len(self.__mesh)

        return 0

    def check_bound(self, dot: Dot) -> bool:
        if self.__x[0] < dot.x() < self.__x[1] and self.__y[0] < dot.y() < self.__y[1]:
            return True

        return False

    def left_bound(self, dot: Dot, y_axis: bool = False) -> bool:
        if y_axis:
            return True if dot.y() == self.__y[0] else False

        return True if dot.x() == self.__x[0] else False

    def right_bound(self, dot: Dot, y_axis: bool = False) -> bool:
        if y_axis:
            return True if dot.y() == self.__y[1] else False

        return True if dot.x() == self.__x[1] else False

    def get_x(self, element: int, index: int):
        return self.__mesh[element][index].x()

    def get_y(self, element: int, index: int):
        return self.__mesh[element][index].y()

    def _node_exists(self, nodes: List[Node], index: int) -> bool:
        if index < len(nodes):
            return True

        return False

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

    def _get_node(self, nodes: List[Node], index: int, position: int, target_pos: int, shift: int = 0) -> Dot:
        if self._node_exists(nodes, index + shift) and index % self.width() != self.width() - 1:
            return nodes[index + shift]

        else:
            return self._make_dot(nodes, index, position, target_pos)

    def _left_x(self, nodes: List[Node], index: int) -> List[Dot]:
        # returns a rectangle to the left of Node beyond the left boundary of x
        return [
            self._make_dot(nodes, index, 3, 0),
            self._make_dot(nodes, index, 3, 1),
            self._get_node(nodes, index, 3, 2, self.width()),
            nodes[index]
        ]

    def _right_x(self, nodes: List[Node], index: int) -> List[Dot]:

        return [
            nodes[index],
            self._get_node(nodes, index, 0, 1, self.width()),
            self._make_dot(nodes, index, 0, 2),
            self._make_dot(nodes, index, 0, 3)
        ]

    def _left_y(self, nodes: List[Node], index: int) -> List[Dot]:

        return [
            self._make_dot(nodes, index, 1, 0),
            nodes[index],
            self._get_node(nodes, index, 1, 2, 1),
            self._make_dot(nodes, index, 1, 3)
        ]

    def _right_y(self, nodes: List[Node], index: int) -> List[Dot]:

        return [
            nodes[index],
            self._make_dot(nodes, index, 0, 1),
            self._make_dot(nodes, index, 0, 2),
            self._get_node(nodes, index, 0, 3, 1)
        ]

    def _first_rect(self, nodes: List[Node], index: int) -> List[Dot]:

        return [
            self._make_dot(nodes, index, 2, 0),
            self._make_dot(nodes, index, 2, 1),
            nodes[index],
            self._make_dot(nodes, index, 2, 3)
        ]

    def _arrange_rect(self, nodes: List[Node], index: int) -> List[List[Dot]]:

        rects = []

        # in node is on the edges of determined area (lies on the lines determined by x and y interval border values)
        if not self.check_bound(nodes[index]):
            # if node is on the left border of x interval
            if self.left_bound(nodes[index]):
                rects.append(self._left_x(nodes, index))

            # if node is on the left border of y interval
            if self.left_bound(nodes[index], True):
                rects.append(self._left_y(nodes, index))

            # if node is on both x and y left borders
            if len(rects) >= 2:
                rects.append(self._first_rect(nodes, index))

            # ----------------------------------------------------------------------------------------------------------

            # if node is on the right border of x interval
            if self.right_bound(nodes[index]):
                rects.append(self._right_x(nodes, index))

                return rects

            # if node is on the right border of y interval
            if self.right_bound(nodes[index], True):
                rects.append(self._right_y(nodes, index))

                return rects

        rects.append(
            [nodes[index],
             self._get_node(nodes, index, 0, 1, self.width()),
             self._get_node(nodes, index, 0, 2, self.width() + 1),
             self._get_node(nodes, index, 0, 3, 1),
             ]
        )

        return rects

    def map_mesh(self, nodes: List[Node]) -> None:

        mesh = []

        for i in range(len(nodes)):
            rects = self._arrange_rect(nodes, i)
            for rect in rects:
                print(rect)
                mesh.append(Rectangle(rect))
            print()

        self.__mesh = mesh

    def basis(self, nodes: List[Node]) -> Basis:
        constants = []

        for node in nodes:
            if str(node) in self.__mesh:
                constants.append(self._constant(str(node)))

        return Basis(constants)

    def _constant(self, node: str):
        constants = dict()

        constants["k"] = self._diagonal(node)
        constants["h_x"] = self.__mesh[node][2].side()
        constants["h_y"] = self.__mesh[node][2].side(True)

        return constants

    def _down_left(self, node: Node) -> List[List[Dot]]:
        rect = [[None, None], [None, None]]

        rect[0][0] = Dot(node.x() - 1, node.y() - 1)
        rect[1][0] = Dot(node.x() - 1, node.y())
        rect[1][1] = node
        rect[0][1] = Dot(node.x(), node.y() - 1)

        return rect

    def _up_left(self, node: Node) -> List[List[Dot]]:
        rect = [[None, None], [None, None]]

        rect[0][0] = Dot(node.x() - 1, node.y())
        rect[1][0] = Dot(node.x() - 1, node.y() + 1)
        rect[1][1] = Dot(node.x(), node.y() + 1)
        rect[0][1] = node

        return rect

    def _up_right(self, node: Node) -> List[List[Dot]]:
        rect = [[None, None], [None, None]]

        rect[0][0] = node
        rect[1][0] = Dot(node.x(), node.y() + 1)
        rect[1][1] = Dot(node.x() + 1, node.y() + 1)
        rect[0][1] = Dot(node.x() + 1, node.y())

        return rect

    def _down_right(self, node: Node) -> List[List[Dot]]:
        rect = [[None, None], [None, None]]

        rect[0][0] = Dot(node.x(), node.y() - 1)
        rect[1][0] = node
        rect[1][1] = Dot(node.x() + 1, node.y())
        rect[0][1] = Dot(node.x() + 1, node.y() - 1)

        return rect

    def _diagonal(self, node: str, rect: int = 2) -> Dot:
        rects = self.__mesh[node]

        # node is upper-right
        if rect == 0:
            return rects[rect].lower_left()

        # node is lower-right
        if rect == 1:
            return rects[rect].upper_left()

        # node is lower-left
        if rect == 2:
            return rects[rect].upper_right()

        # node is upper-left
        return rects[rect].lower_right()
