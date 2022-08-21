from Interfaces.matrix_interface import IMatrix

import numpy as np


# Matrix wrapper class for calculations
class Matrix(IMatrix):
    def __init__(self, rows: int, columns: int, data: np.array = None):
        # self.__rows = rows
        # self.__columns = columns
        self.__matrix = self.__create(rows, columns)

        if data is not None:
            if self.__check(data):
                self.__matrix = data
            else:
                raise ValueError(f"Given shape {self.rows(), self.columns()} doesn't match given array's {data.shape}!")

    @staticmethod
    def __create(rows: int, columns: int) -> np.array:
        return np.zeros((rows, columns))

    # Checks the given arrays shape to be compatible with own shape.
    def __check(self, data: np.array) -> bool:
        if self.rows() == data.shape[0] and self.rows() == data.shape[1]:
            return True

        return False

    def rows(self) -> int:
        return self.__matrix.shape[0]

    def columns(self) -> int:
        return self.__matrix.shape[1]

    def fill(self) -> None:
        pass

    def get_data(self) -> np.array:
        return self.__matrix

    # changes all the matrix's values to ones from array if the given array's dimensions are compatible
    def update_data(self, data: np.array) -> None:
        if self.__check(data):
            self.__matrix = data
        else:
            raise ValueError(f"Array's dimensions {data.shape} don't match matrix's {self.rows(), self.columns()}!")

    def merge(self, data: np.array, axis: int = 0) -> None:
        if self.__check(data):

            if axis == 0:
                self.__matrix = np.concatenate((self.__matrix, data))
            else:
                self.__matrix = np.concatenate((self.__matrix, data), axis=1)
        else:
            if axis == 0 and self.columns() == data.shape[1]:
                self.__matrix = np.concatenate((self.__matrix, data))

            elif axis == 1 and self.rows() == data.shape[0]:
                self.__matrix = np.concatenate((self.__matrix, data), axis=1)

            else:
                raise ValueError(f"Cannot merge {data.shape} array with {self.rows(), self.columns()} matrix along"
                                 f" the given axis!")

    # changes a single value within the matrix
    def change_value(self, row: int, column: int, value: float) -> None:
        if self(row, column) is not None:
            self.__matrix[row][column] = value

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
                return self.__matrix[row][column]
            else:
                raise IndexError(f"column index ({column}) out of range!")
        else:
            raise IndexError(f"row index ({row}) out of range!")