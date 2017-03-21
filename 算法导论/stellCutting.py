import numpy as np


def MemoizedCutRod(p, n):
    r = np.zeros(n)
    for i in range(r):
        r[i] = -10000
    return MemoizedCutRodAux(p, n, r)


def MemoizedCutRodAux(p, n, r):
	q = 0
    if r[n - 1] >= 0:
        return r[n - 1]
    if n == 0:
        q == 0
    else:
        q == -10000
        for i in range(n):
            q = max(q, p[i] + MEMOIZED - CUT - ROD - AUX(p, n - i, r))
    r[n - 1] = q
    return q
p = np.array([1, 5, 8, 9, 10, 17, 17, 20, 24, 30])
n = len(q)
print MemoizedCutRod(p, n)
