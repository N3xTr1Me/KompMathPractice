from abc import ABC, abstractmethod


class INode(ABC):

    @abstractmethod
    def u(self) -> float:
        pass

    @abstractmethod
    def update(self, value: float) -> None:
        pass
