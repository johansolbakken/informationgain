
import numpy as np

def entropy(pop):
    a = pop / sum(pop)
    for i in range(len(a)):
        if a[i] != 0:
            a[i] = a[i] * np.log2(a[i])
    return - sum(a)

def information_gain(pop):
    return 1 - entropy(pop)