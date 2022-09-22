from typing import List, Dict

from Data.basis.basis import Basis
from Data.basis.local_basis.nodal_function import Psi
from Data.basis.local_basis.nodal_derivative import DPsi


class Elemental(Basis):
    def __init__(self, constants: List[Dict[str, float]]):
        super(Elemental, self).__init__(constants)

    def _make_function(self, constant: Dict[str, float]):
        return Psi(constant)

    def _make_derivative(self, constant: Dict[str, float]):
        return DPsi(constant)
