from Interfaces.matrix_interface import IMatrix

import numpy as np


# Matrix wrapper class for calculations
class Matrix(IMatrix):
    def __init__(self, rows: int, columns: int, data: np.array = None):
        self.__rows = rows
        self.__columns = columns
        self.__matrix = None

        if data is not None:
            if self.__check(data):
                self.__matrix = data
            else:
                raise ValueError(f"Given shape {self.__rows, self.__columns} "
                                 f"doesn't match given array's {data.shape}!")
        else:
            self.fill()

    # Checks the given arrays shape to be compatible with own shape.
    def __check(self, data: np.array) -> bool:
        if self.__rows == data.shape[0] and self.__columns == data.shape[1]:
            return True
        return False

    def rows(self) -> int:
        return self.__rows

    def columns(self) -> int:
        return self.__columns

    # Fills matrix with values (zeroes).
    def fill(self) -> None:
        self.__matrix = np.zeros((self.rows(), self.columns()))

    def get_data(self) -> np.array:
        return self.__matrix

    # changes all the matrix's values to ones from array
    # if the given array's dimensions are compatible
    def update_data(self, data: np.array) -> None:
        if self.__check(data):
            self.__matrix = data
        else:
            raise ValueError(
                f"Array's dimensions {data.shape} don't match matrix's "
                f"{self.rows(), self.columns()}!")

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
            raise ValueError(f"Cannot perform multiplication with shapes: "
                             f"{self.rows(), self.columns()} and "
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

    def __str__(self):
        output = ""
        for i in range(self.rows()):
            for j in range(self.columns()):
                output += str(self.__matrix[i][j]) + "\t"
            output += "\n"
        return output
