from abc import ABC, abstractmethod


class INodal(ABC):

    @abstractmethod
    def a(self) -> float:
        pass

    @abstractmethod
    def b(self) -> float:
        pass

    @abstractmethod
    def c(self) -> float:
        pass
    
    @abstractmethod
    def f(self) -> callable:
        pass

    @abstractmethod
    def __call__(self, x: float, y: float) -> float:
        pass
