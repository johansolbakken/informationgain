import numpy as np


def entropy(pop: np.ndarray):
    if sum(pop) == 0:
        return 0
    a = pop / sum(pop)
    for i in range(len(a)):
        if a[i] != 0:
            a[i] = a[i] * np.log2(a[i])
    return - sum(a)


def information_gain(pop: np.ndarray):
    return 1 - entropy(pop)
