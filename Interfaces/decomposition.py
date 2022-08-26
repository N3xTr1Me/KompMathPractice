from abc import ABC, abstractmethod
from typing import Dict
import numpy


class IDecomposition(ABC):

    @abstractmethod
    def LU(self) -> Dict[str, numpy.array]:
        pass

    @abstractmethod
    def LUP(self) -> Dict[str, numpy.array]:
        pass
