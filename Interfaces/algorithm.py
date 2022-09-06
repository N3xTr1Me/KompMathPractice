from abc import ABC, abstractmethod

from Data.matrices.matrix import Matrix
from Data.matrices.mass_matrix import MassMatrix
from Data.matrices.stiffness_matrix import StiffnessMatrix

from Model.frame import Frame


class IAlgorithm(ABC):

    @abstractmethod
    def __mass(self) -> MassMatrix:
        pass

    @abstractmethod
    def __stiffness(self) -> StiffnessMatrix:
        pass

    @abstractmethod
    def __b(self) -> Matrix:
        pass

    @abstractmethod
    def __k(self, current: Frame, t: float) -> float:
        pass

    @abstractmethod
    def __build_frame(self, xi: Matrix, t: float, mass: MassMatrix, stiff: StiffnessMatrix) -> Frame:
        pass

    @abstractmethod
    def step(self, t: float, previous: Frame) -> Frame:
        pass
