from Interfaces.matrix_interface import IMatrix
from Interfaces.decomposition import IDecomposition

from typing import Dict
from copy import deepcopy
import numpy as np


# Matrix wrapper class for calculations
class Matrix(IMatrix, IDecomposition):
    def __init__(self, rows: int, columns: int, data: np.array = None):
        super(Matrix, self).__init__()

        self._rows = rows
        self._columns = columns

        if data is not None:
            if self.__check(data):
                self._matrix = data
            else:
                raise ValueError(f"Given shape {self._rows, self._columns} doesn't match given array's {data.shape}!")
        else:
            self._matrix = None

    # ------------------------------------------------------------------------------------------------------------------
    #                                        Basic functionality
    # ------------------------------------------------------------------------------------------------------------------

    # Checks the given arrays shape to be compatible with own shape.
    def __check(self, data: np.array) -> bool:
        if self._rows == data.shape[0] and self._columns == data.shape[1]:
            return True

        return False

    def rows(self) -> int:
        return self._rows

    def columns(self) -> int:
        return self._columns

    # Fills matrix with values (zeroes).
    def _fill(self) -> None:
        self._matrix = np.zeros((self.rows(), self.columns()))

    # ------------------------------------------------------------------------------------------------------------------
    #                                        Data manipulation
    # ------------------------------------------------------------------------------------------------------------------

    def get_data(self) -> np.array:
        return self._matrix

    # changes all the matrix's values to ones from array
    # if the given array's dimensions are compatible
    def update_data(self, data: np.array) -> None:
        if self.__check(data):
            self._matrix = data
        else:
            raise ValueError(f"Array's dimensions {data.shape} don't match matrix's {self.rows(), self.columns()}!")

    def _update_dimensions(self, rows: int, columns: int) -> None:

        if self.rows() != rows:
            self._rows = rows

        if self.columns() != columns:
            self._columns = columns

    def merge(self, data: np.array, axis: int = 0) -> None:
        if self.__check(data):

            if axis == 0:
                self._matrix = np.concatenate((self._matrix, data))
            else:
                self._matrix = np.concatenate((self._matrix, data), axis=1)
        else:
            if axis == 0 and self.columns() == data.shape[1]:
                self._matrix = np.concatenate((self._matrix, data))

            elif axis == 1 and self.rows() == data.shape[0]:
                self._matrix = np.concatenate((self._matrix, data), axis=1)

            else:
                raise ValueError(f"Cannot merge {data.shape} array with {self.rows(), self.columns()} matrix along"
                                 f" the given axis!")

        self._update_dimensions(data.shape[0], data.shape[1])

    # changes a single value within the matrix
    def change_value(self, row: int, column: int, value: float) -> None:
        if self(row, column) is not None:
            self._matrix[row][column] = value

    # ------------------------------------------------------------------------------------------------------------------
    #                                        Matrix decomposition
    # ------------------------------------------------------------------------------------------------------------------

    def LU(self, matrix: np.array = None) -> Dict[str, np.array]:

        if matrix is None:
            matrix = self._matrix

        rows, columns = len(matrix), len(matrix[0])

        L, U = np.zeros((rows, rows)), np.zeros((rows, columns))

        U[0][0] = matrix[0][0]
        L[0][0] = 1

        if len(matrix) > 1 or len(matrix[0]) > 1:
            U[0:1, 1:len(U[0])] = matrix[0:1, 1:len(U[0])]
            L[1:len(L), 0:1] = matrix[1:len(L), 0:1] / U[0][0]
            small_rectangle = matrix[1:len(matrix), 1: len(matrix[0])] - L[1:len(L), 0:1] * U[0:1, 1:len(U[0])]

            if len(matrix) > 1 and len(matrix[0]) > 1:
                result = self.LU(small_rectangle)
                L[1:len(L), 1:len(L[0])], U[1:len(U), 1:len(U[0])] = result["L"], result["U"]

        return {"L": L, "U": U}

    def LUP(self, matrix: np.array = None) -> Dict[str, np.array]:
        if matrix is None:
            matrix = self._matrix

        n = max(len(matrix), len(matrix[0]))
        C = deepcopy(matrix)

        P = np.eye(n)

        for i in range(n):
            pivotValue = 0
            pivot = -1
            for row in range(i, n):
                if abs(C[row][i]) > pivotValue:
                    pivotValue = abs(C[row][i])
                    pivot = row

            if pivotValue != 0:
                P[pivot], P[i] = deepcopy(P[i]), deepcopy(P[pivot])
                C[pivot], C[i] = deepcopy(C[i]), deepcopy(C[pivot])
                for j in range(i + 1, n):
                    C[j][i] /= C[i][i]
                    for k in range(i + 1, n):
                        C[j][k] -= C[j][i] * C[i][k]

        L = np.zeros((n, n))
        U = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                if i > j:
                    L[i][j] = C[i][j]
                else:
                    U[i][j] = C[i][j]
                    L[i][i] = 1

        return {"L": L, "U": U, "P": P}

    # ------------------------------------------------------------------------------------------------------------------
    #                                        object functions overriding
    # ------------------------------------------------------------------------------------------------------------------

    def __add__(self, other):
        if self.rows() == other.rows() and self.columns() == other.columns():

            new_matrix = self.get_data() + other.get_data()
            return Matrix(rows=self.rows(), columns=self.columns(), data=new_matrix)

        else:
            raise ValueError(f"Matrices' dimensions don't match: {self.rows(), self.columns()} / "
                             f"{other.rows(), other.columns()}!")

    def __mul__(self, other):
        if self.columns() == other.rows():
            new_matrix = np.dot(self.get_data(), other.get_data())
            return Matrix(rows=self.rows(), columns=other.columns(), data=new_matrix)

        else:
            raise ValueError(f"Cannot perform multiplication with shapes: {self.rows(), self.columns()} and "
                             f"{other.rows(), other.columns()}!")

    # allows calling matrix objects by indexes
    def __call__(self, row: int, column: int):
        if 0 <= row < self.rows():
            if 0 <= column < self.columns():
                return self._matrix[row][column]
            else:
                raise IndexError(f"column index ({column}) out of range!")
        else:
            raise IndexError(f"row index ({row}) out of range!")

    def __str__(self):
        output = ""
        for i in range(self.rows()):
            for j in range(self.columns()):
                output += str(self._matrix[i][j]) + "\t"
            output += "\n"
        return output


exp1 = [
    [2, 7, -6],
    [8, 2, 1],
    [7, 4, 2]
]

current_example = np.array(exp1)

mat = Matrix(3, 3, current_example)
print(mat.LUP())
