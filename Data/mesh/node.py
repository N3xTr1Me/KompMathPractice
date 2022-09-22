from Interfaces.mesh.node_interface import INode

from Data.grid.dot import Dot


# a node-dot on the 2D grid. Has (x,y) coordinates, a set of basis functions and nodal value, holds 2 neighboring
# node's coordinates
class Node(INode, Dot):
    def __init__(self, x: int, y: int, value: float):
        super(Node, self).__init__(x, y)

        self.__u = value
        self.__connected = 0

    def u(self) -> float:
        return self.__u

    def update(self, value: float) -> None:
        self.__u = value

    def connect(self) -> None:
        self.__connected += 1
        
    def connected(self) -> int:
        return self.__connected
