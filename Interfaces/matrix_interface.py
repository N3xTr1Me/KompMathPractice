from abc import ABC, abstractmethod

from numpy import array


class IMatrix(ABC):
    @abstractmethod
    def fill(self) -> None:
        pass

    @abstractmethod
    def rows(self) -> int:
        pass

    @abstractmethod
    def columns(self) -> int:
        pass

    @abstractmethod
    def get_result(self) -> array:
        pass
