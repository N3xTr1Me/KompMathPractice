from abc import ABC, abstractmethod
from typing import Tuple
import numpy


class IDecomposition(ABC):

    @abstractmethod
    def LU(self) -> Tuple[numpy.array]:
        pass

    @abstractmethod
    def LUP(self) -> Tuple[numpy.array]:
        pass
  