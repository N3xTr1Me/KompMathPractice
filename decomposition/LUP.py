from copy import deepcopy

from decomposition.LU import lu

import numpy as np


def lup(A):
    n = max(len(A), len(A[0]))
    C = deepcopy(A)

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

    return L, U, P


if __name__ == "__main__":
    exp1 = [
        [2, 7, -6],
        [8, 2, 1],
        [7, 4, 2]
    ]

    current_example = exp1

    LUP = lup(current_example)

    L, U, P = LUP[0], LUP[1], LUP[2]

    print("L")
    print(L)
    print()
    print("U")
    print(U)
    print()
    print("P")
    print(P)
