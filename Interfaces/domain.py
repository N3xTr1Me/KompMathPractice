from abc import ABC, abstractmethod


class IDomain(ABC):

    @abstractmethod
    def within(self, x: float, y: float) -> bool:
        pass
