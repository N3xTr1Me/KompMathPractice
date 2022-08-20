from abc import ABC, abstractmethod

from numpy import array


class IMatrix(ABC):
    @abstractmethod
    def fill(self) -> None:
        pass

    @abstractmethod
    def height(self) -> int:
        pass

    @abstractmethod
    def width(self) -> int:
        pass

    @abstractmethod
    def get_result(self) -> array:
        pass
