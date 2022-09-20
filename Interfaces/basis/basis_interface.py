from abc import ABC, abstractmethod


class IBasis(ABC):

    @abstractmethod
    def phi(self, x: float, y: float) -> float:
        pass

    @abstractmethod
    def d_phi(self, x: float, y: float) -> float:
        pass

    @abstractmethod
    def __call__(self, x: float, y: float, derivative: bool = False) -> float:
        pass
