from abc import ABC, abstractmethod

from Data.matrices.matrix import Matrix
from Data.matrices.mass_matrix import MassMatrix
from Data.matrices.stiffness_matrix import StiffnessMatrix

from Model.frame import Frame


class IAlgorithm(ABC):

    @abstractmethod
    def _mass(self) -> MassMatrix:
        pass

    @abstractmethod
    def _stiffness(self) -> StiffnessMatrix:
        pass

    @abstractmethod
    def _b(self) -> Matrix:
        pass

    @abstractmethod
    def _k(self, current: Frame, t: float) -> float:
        pass

    @abstractmethod
    def _build_frame(self, xi: Matrix, t: float, mass: MassMatrix, stiff: StiffnessMatrix) -> Frame:
        pass

    @abstractmethod
    def step(self, t: float, previous: Frame) -> Frame:
        pass
