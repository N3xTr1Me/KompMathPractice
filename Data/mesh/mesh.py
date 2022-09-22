from typing import List, Tuple, Dict

from Data.basis.basis import Basis
from Data.mesh.cell import Cell
from Data.mesh.node import Node
from Data.grid.dot import Dot
from Data.mesh.rectangle import Rectangle


class Mesh:
    def __init__(self, width: int, height: int, nodes: List[Node]):

        self.__w = width
        self.__h = height

        self.__mesh = dict()
        self.map_mesh(nodes)

    def width(self) -> int:
        return self.__w

    def height(self) -> int:
        return self.__h

    def check_bound(self, dot: Dot) -> bool:
        if 0 < dot.x() <= self.__w and 0 < dot.y() <= self.__h:
            return True

        return False

    def map_mesh(self, nodes: List[Node]) -> None:

        connections = dict()

        for node in nodes:
            self.__mesh[str(node)] = [
                Rectangle(self._down_left(node)), Rectangle(self._up_left(node)),
                Rectangle(self._up_right(node)), Rectangle(self._down_right(node)),
            ]

            connections[str(node)] = node

        connections = self.change_neighbours(connections)
        new_mesh = {node: [] for node in self.__mesh}

        for node in self.__mesh:
            for i in range(len(self.__mesh[node])):
                if i in connections[node]:
                    new_mesh[node].append(Cell(self.__mesh[node][i], connections[node][i]))
                else:
                    new_mesh[node].append(Cell(self.__mesh[node][i]))

        self.__mesh = new_mesh

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

    def _diagonal(self, node: str, rectangle: int = 2) -> Dot:
        rects = self.__mesh[node]

        # node is upper-right
        if rectangle == 0:
            return rects[rectangle].lower_left()

        # node is lower-right
        if rectangle == 1:
            return rects[rectangle].upper_left()

        # node is lower-left
        if rectangle == 2:
            return rects[rectangle].upper_right()

        # node is upper-left
        return rects[rectangle].lower_right()


_nodes = [Node(1, 1, -12), Node(2, 2, 5), Node(3, 2, -8), Node(2, 3, 0)]
mesh = Mesh(4, 4, _nodes)
# k = mesh.basis(_nodes)
print()
