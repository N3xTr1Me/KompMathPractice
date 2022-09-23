from typing import List, Tuple, Dict

from Data.basis.basis import Basis
from Data.mesh.cell import Cell
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
        return self.__x[1] - self.__x[0]

    def height(self) -> int:
        return self.__y[1] - self.__y[0]

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
        if self.check_x(dot) and self.check_y(dot):
            return True

        return False

    def check_x(self, dot: Dot) -> bool:
        if self.__x[0] <= dot.x() <= self.__x[1]:
            return True

        return False

    def check_y(self, dot: Dot) -> bool:
        if self.__y[0] <= dot.y() <= self.__y[1]:
            return True

        return False

    def get_x(self, element: int, index: int):
        return self.__mesh[element][index].x()

    def get_y(self, element: int, index: int):
        return self.__mesh[element][index].y()

    def _arrange_rect(self, nodes: List[Node], index: int) -> List[Dot]:

        if index % self.width() == self.width() - 1:
            return [nodes[index],
                    nodes[index + self.width()],
                    Dot(nodes[index].x() + self.x_step(), nodes[index].y() + self.y_step()),
                    Dot(nodes[index].x() + self.x_step(), nodes[index].y())
                    ]

        return [nodes[index],  # lower-left aka the current node
                nodes[index + self.width()],  # upper-left node
                nodes[index + self.width() + 1],  # upper-right node
                nodes[index + 1]  # lower-left node
                ]

    def map_mesh(self, nodes: List[Node]) -> None:

        mesh = []

        for i in range(len(nodes) - self.width()):

            if self.check_bound(nodes[i]):
                vertexes = self._arrange_rect(nodes, i)
                mesh.append(Rectangle(vertexes))

        self.__mesh = mesh

    def change_neighbours(self, nodes: Dict[str, Node]):

        connections = {node: {} for node in nodes}

        for node in nodes:
            rects = self.__mesh[node]

            for i in range(len(rects)):
                x_side, y_side = rects[i].side(), rects[i].side(True)

                # node is upper-right
                if i == 0:
                    up_left = f"{nodes[node].x() - x_side, nodes[node].y()}"
                    low_right = f"{nodes[node].x(), nodes[node].y() - y_side}"
                    if up_left in nodes:
                        rects[i].update_dot(x=0, y=1, dot=nodes[up_left])
                        connections[node][i] = 0, 1

                    if low_right in nodes:
                        rects[i].update_dot(x=1, y=0, dot=nodes[low_right])
                        connections[node][i] = 1, 0

                # node is lower-right
                elif i == 1:
                    up_right = f"{nodes[node].x(), nodes[node].y() + y_side}"
                    low_left = f"{nodes[node].x() - x_side, nodes[node].y()}"
                    if up_right in nodes:
                        rects[i].update_dot(x=1, y=1, dot=nodes[up_right])
                        connections[node][i] = 1, 1

                    if low_left in nodes:
                        rects[i].update_dot(x=0, y=0, dot=nodes[low_left])
                        connections[node][i] = 0, 0

                # node is lower-left
                elif i == 2:
                    up_left = f"{nodes[node].x(), nodes[node].y() + y_side}"
                    low_right = f"{nodes[node].x() + x_side, nodes[node].y()}"
                    if up_left in nodes:
                        rects[i].update_dot(x=0, y=1, dot=nodes[up_left])
                        connections[node][i] = 0, 1

                    if low_right in nodes:
                        rects[i].update_dot(x=1, y=0, dot=nodes[low_right])
                        connections[node][i] = 1, 0

                # node is upper-left
                else:
                    up_right = f"{nodes[node].x() + x_side, nodes[node].y()}"
                    low_left = f"{nodes[node].x(), nodes[node].y() - y_side}"
                    if up_right in nodes:
                        rects[i].update_dot(x=1, y=1, dot=nodes[up_right])
                        connections[node][i] = 1, 1

                    if low_left in nodes:
                        rects[i].update_dot(x=0, y=0, dot=nodes[low_left])
                        connections[node][i] = 0, 0

        return connections

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
