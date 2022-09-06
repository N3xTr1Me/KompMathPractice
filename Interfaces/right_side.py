from abc import ABC, abstractmethod


class IRightSide(ABC):

    @abstractmethod
    def within(self, x: float, y: float) -> bool:
        pass

    @abstractmethod
    def __call__(self, x: float, y: float) -> float:
        pass
