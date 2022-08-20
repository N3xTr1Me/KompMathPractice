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
    def get_data(self) -> array:
        pass

    @abstractmethod
    def update_data(self, data: array) -> None:
        pass

    @abstractmethod
    def change_value(self, row: int, column: int, value: float) -> None:
        pass
 