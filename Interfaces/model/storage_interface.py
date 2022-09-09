from abc import ABC, abstractmethod

from Model.algorithm.frame import Frame


class IStorage(ABC):

    @abstractmethod
    def write(self, path: str, data, rewrite: bool = False) -> None:
        pass

    @abstractmethod
    def read(self, path: str) -> dict:
        pass

    @abstractmethod
    def set_config(self, options: dict = None, path: str = None) -> None:
        pass

    @abstractmethod
    def get_config(self, path: str = None) -> dict:
        pass

    @abstractmethod
    def start_session(self) -> str:
        pass

    @abstractmethod
    def set_storage(self, path: str) -> None:
        pass

    @abstractmethod
    def store(self, session: str, step: Frame) -> None:
        pass

    @abstractmethod
    def get_step(self, session: str, step: float) -> Frame:
        pass
