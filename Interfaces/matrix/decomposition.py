from abc import ABC, abstractmethod
from typing import Dict
import numpy


class IDecomposition(ABC):

    @abstractmethod
    def LU(self, matrix: numpy.array = None) -> Dict[str, numpy.array]:
        pass

    @abstractmethod
    def LUP(self, matrix: numpy.array = None) -> Dict[str, numpy.array]:
        pass
