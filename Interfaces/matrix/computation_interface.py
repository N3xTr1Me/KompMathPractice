from abc import ABC, abstractmethod

from Data.mesh.mesh import Mesh

from numpy import array


class IComputable(ABC):

    @abstractmethod
    def _fill(self, elements: int):
        pass

    @abstractmethod
    def _get_from_src(self, k: int) -> array:
        pass
