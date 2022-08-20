from Interfaces.matrix_interface import IMatrix

import numpy as np


class Matrix(IMatrix):
    def __init__(self, rows: int, columns: int, data: np.array):
        self.__rows = rows
        self.__columns = columns
        self.__matrix = None

        if data:
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

    def get_result(self) -> np.array:
        return self.__matrix

    def __add__(self, other):
        if self.rows() == other.rows() and self.columns() == other.columns():

            new_matrix = self.get_result() + other.get_result()
            return Matrix(rows=self.rows(), columns=self.columns(), data=new_matrix)

        else:
            raise ValueError(f"Matrices' dimensions don't match: {self.rows(), self.columns()}/"
                             f"{other.rows(), other.columns()}!")

    def __mul__(self, other):
        if self.columns() == other.rows():
            new_matrix = np.dot(self.get_result(), other.get_result())
            return Matrix(rows=self.rows(), columns=other.columns(), data=new_matrix)

        else:
            raise ValueError(f"Cannot perform multiplication with shapes: {self.rows(), self.columns()} and"
                             f"{other.rows(), other.columns()}!")
