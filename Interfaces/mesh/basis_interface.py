from abc import ABC, abstractmethod


class IBasis(ABC):

    @abstractmethod
    def phi_1(self, x: float, y: float, w: int, h: int) -> float:
        pass

    @abstractmethod
    def phi_2(self, x: float, y: float, w: int, h: int) -> float:
        pass

    @abstractmethod
    def d_phi_1(self, x: float, y: float, w: int, h: int) -> float:
        pass

    @abstractmethod
    def d_phi_2(self, x: float, y: float, w: int, h: int) -> float:
        pass
