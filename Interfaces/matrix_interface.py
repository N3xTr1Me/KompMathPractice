from abc import ABC, abstractmethod

import numpy as np


class IMatrix(ABC):
    @abstractmethod
    def _fill(self) -> None:
        pass

    @abstractmethod
    def rows(self) -> int:
        pass

    @abstractmethod
    def columns(self) -> int:
        pass

    @abstractmethod
    def get_data(self) -> np.array:
        pass

    @abstractmethod
    def update_data(self, data: np.array) -> None:
        pass

    @abstractmethod
    def change_value(self, row: int, column: int, value: float) -> None:
        pass

    @abstractmethod
    def merge(self, data: np.array, axis: int = 0) -> None:
        pass

    @abstractmethod
    def _update_dimensions(self) -> None:
        pass
