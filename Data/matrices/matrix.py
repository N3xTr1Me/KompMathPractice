from Interfaces.matrix_interface import IMatrix

import numpy as np


class Matrix(IMatrix):
    def __init__(self, rows: int, columns: int, data: np.array = None):
        self.__rows = rows
        self.__columns = columns
        self.__matrix = None

        if data is not None:
            if self.__check(data):
                self.__matrix = data
            else:
                raise ValueError(f"Given shape {self.__rows, self.__columns} doesn't match given array's {data.shape}!")
        else:
            self.fill()

    def __check(self, data: np.array):
        if self.__rows == data.shape[0] and self.__columns == data.shape[1]:
            return True

        return False

    def rows(self) -> int:
        return self.__rows

    def columns(self) -> int:
        return self.__columns

    def fill(self) -> None:
        self.__matrix = np.zeros((self.rows(), self.columns()))

    def get_data(self) -> np.array:
        return self.__matrix

    def update_data(self, data: np.array) -> None:
        if self.__check(data):
            self.__matrix = data
        else:
            raise ValueError(f"Array's dimensions {data.shape} don't match matrix's {self.rows(), self.columns()}!")

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

    def __call__(self, row: int, column: int):
        if 0 <= row < self.rows():
            if 0 <= column < self.columns():
                return self.__matrix[row][column]
            else:
                raise IndexError(f"column index ({column}) out of range!")
        else:
            raise IndexError(f"row index ({row}) out of range!")
