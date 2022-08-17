from math import pi, exp
from random import randint
import matplotlib.pyplot as plt
import seaborn as sns
from copy import deepcopy

A = 10
B = 10
max_temperature = 10

a = [[0] * A for _ in range(B)]

for i in range(B):
    for j in range(A):
        a[i][j] = randint(1, max_temperature)

new_a = [[0] * A for _ in range(B)]

for t in range(1, 30):
    t /= 2
    for i in range(B):
        for j in range(A):
            T = [[0] * A for _ in range(B)]
            for x1 in range(B):
                for x2 in range(A):
                    T[x1][x2] = a[x1][x2] * exp(-1 / 4 / t * ((i - x1) * 2 + (j - x2) * 2))
            s = sum([sum(i) for i in T]) / 4 / pi / t
            new_a[i][j] = s
    a = deepcopy(new_a)
    sns.color_palette("magma", as_cmap=True)
    sns.heatmap(a, vmin=0, vmax=max_temperature)
    plt.show()
