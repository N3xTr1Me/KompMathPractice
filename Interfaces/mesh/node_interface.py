from abc import ABC, abstractmethod

from typing import Tuple


class INode(ABC):

    @abstractmethod
    def coords(self) -> Tuple[float, float]:
        pass

    @abstractmethod
    def j(self) -> Tuple[float, float]:
        pass

    @abstractmethod
    def k(self) -> Tuple[float, float]:
        pass

    @abstractmethod
    def u(self) -> float:
        pass

    @abstractmethod
    def set_u(self, value: float) -> None:
        pass

    @abstractmethod
    def phi(self, x: float, y: float) -> float:
        pass

    @abstractmethod
    def d_phi(self, x: float, y: float) -> float:
        pass
