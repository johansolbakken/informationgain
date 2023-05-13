from information_gain_app.decision_tree.information_gain import *


def test_entropy():
    pop = np.array([1, 1, 1, 1])
    assert entropy(pop) == 2.0


def test_information_gain():
    pop = np.array([1, 1, 1, 1])
    assert information_gain(pop) == -1.0
