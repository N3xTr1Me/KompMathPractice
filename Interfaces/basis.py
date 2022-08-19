from abc import ABC, abstractmethod


class IBasis(ABC):

    @abstractmethod
    def basis(self, function: str) -> callable:
        pass

    @abstractmethod
    def phi_1(self) -> callable:
        pass

    @abstractmethod
    def phi_2(self) -> callable:
        pass

    @abstractmethod
    def d_phi_1(self) -> callable:
        pass

    @abstractmethod
    def d_phi_2(self) -> callable:
        pass
