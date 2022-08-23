from typing import List

from pprint import pprint

import numpy as np


def lu(A: np.array):
    rows, columns = len(A), len(A[0])
    L, U = np.zeros((rows, rows)), np.zeros((rows, columns))
    U[0][0] = A[0][0]
    L[0][0] = 1
    if len(A) > 1 or len(A[0]) > 1:
        U[0:1, 1:len(U[0])] = A[0:1, 1:len(U[0])]
        L[1:len(L), 0:1] = A[1:len(L), 0:1] / U[0][0]
        small_rectangle = A[1:len(A), 1: len(A[0])] - L[1:len(L), 0:1] * U[0:1, 1:len(U[0])]
        if len(A) > 1 and len(A[0]) > 1:
            L[1:len(L), 1:len(L[0])], U[1:len(U), 1:len(U[0])] = lu(small_rectangle)
    return L, U


# Examples
if __name__ == "__main__":
    exp1 = [
        [4, 3],
        [6, 3]
    ]

    exp2 = [
        [4, 0, 1],
        [8, 3, 4],
        [0, -3, -1]
    ]

    exp3 = [
        [1, 2, 3],
        [6, 4, 5]
    ]

    exp4 = [
        [1, 2, 3, 66],
        [6, 4, 5, 1],
        [13, 14, 52, 22]
    ]

    current_experiment = np.array(exp4)

    L, U = lu(current_experiment)

    print("U")
    print(U)

    print()

    print("L")
    print(L)
