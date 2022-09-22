from typing import List

from Data.mesh.node import Node
from Data.grid.dot import Dot
from Data.mesh.rectangle import Rectangle


class Mesh:
    def __init__(self, width: int, height: int, nodes: List[Node]):
        self.__w = width
        self.__h = height

        self.__mesh = dict()
        self.map_mesh(nodes)

    def check_bound(self, dot: Dot) -> bool:
        if 0 < dot.x() <= self.__w and 0 < dot.y() <= self.__h:
            return True

        return False

    def map_mesh(self, nodes: List[Node]) -> None:
        for node in nodes:
            self.__mesh[str(node)] = {"low-left": Rectangle(self._down_left(node)),
                                      "up-left": Rectangle(self._up_left(node)),
                                      "up-right": Rectangle(self._up_right(node)),
                                      "low-right": Rectangle(self._down_right(node))}

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

    def _diagonal(self, node: str, rectangle: str) -> Dot:
        rects = self.__mesh[node]

        if rectangle == "low-left":
            return rects[rectangle].lower_left()

        if rectangle == "up-left":
            return rects[rectangle].upper_left()

        if rectangle == "up-right":
            return rects[rectangle].upper_right()

        return rects[rectangle].lower_right()


_nodes = [Node(1, 1, -12), Node(1, 3, 5), Node(3, 1, -8), Node(3, 3, 0)]
mesh = Mesh(4, 4, _nodes)
print(mesh._diagonal("(3, 1)", "low-left"))
