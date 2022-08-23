from abc import ABC, abstractmethod


class IBorder(ABC):

    @abstractmethod
    def within(self, x: float, y: float) -> bool:
        pass
