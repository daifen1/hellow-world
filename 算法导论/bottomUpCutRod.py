import numpy as np


def cutRod(p, n):
    r = np.zeros(n + 1)
    r[0] = 0
    for j in range(1, n):
        q = 0
        for i in range(j):
            q = max(q, p[i] + r[j - i])
        r[j + 1] = q
    return r[n]

p = np.array([1, 5, 8, 9, 10, 17, 17, 20, 24, 30])
print cutRod(p, 10)
