from math import pi, exp
from random import randint
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from copy import deepcopy
from numba import njit

import datetime


@njit
def solve(a, t):
    new_a = np.zeros((width, height))
    for i in range(height):
        for j in range(width):
            T = [[0] * width for _ in range(height)]
            for x1 in range(height):
                for x2 in range(width):
                    T[x1][x2] = a[x1][x2] * exp(-1 / 4 / t * ((i - x1) * 2 + (j - x2) * 2))
            s = sum([sum(i) for i in T]) / 4 / pi / t
            new_a[i][j] = s
    return new_a


width = 30
height = 30

min_temperature = 0
max_temperature = 10

a = np.zeros((width, height))

for i in range(height):
    for j in range(width):
        a[i][j] = randint(min_temperature, max_temperature)

t1 = datetime.datetime.now()

for i in range(1, 30):
    a = solve(a, i / 10)
    sns.color_palette("magma", as_cmap=True)
    sns.heatmap(a, vmin=min_temperature, vmax=max_temperature)
    plt.show()

print(datetime.datetime.now() - t1)
