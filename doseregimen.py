#!/usr/bin/python
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams['toolbar'] = 'None'
from interval import *
from box import *
from functions import *


class Concentration(object):
    def __init__(self, d, Ka, Ke, V, F):
        self.d = d
        self.Ka = Ka
        self.Ke = Ke
        self.V = V
        self.F = F

    def __call__(self, t):
        d = self.d
        Ka = self.Ka
        Ke = self.Ke
        V = self.V
        F = self.F
        result = Box([0] * len(t))
        result.intervals = [F * d * Ka / (V * (Ka - Ke)) * (exp(-Ke * t[r]) - exp(-Ka * t[r])) for r in
                            range(0, len(t))]
        return (result)


# PK parameters
# Ka = 0.37 (1/h)
# Ke = 0.2  (1/h)
#  V = 24   (L)
#  F = 0.95

def C(t):
    concentration = Concentration(d=Interval(0.01, 250), Ka=0.37, Ke=0.2, V=24, F=0.95)
    return concentration(t)


def plot(t, fun):
    y = fun(t)
    fig = plt.figure()
    fig.set_facecolor("white")

    ax = fig.add_subplot(111)
    for r in range(0, len(t)):
        ax.plot([t[r]] * 2, [y[r].low, y[r].upp], color="k", linewidth=2)
    ax.grid(True)
    plt.show()


t = range(0, 36)
plot(t, C)

for n in range(0, 20):
    print "n = {0}: interval = ".format(n), Interval(np.pi) / (1 + 1.0 / 10 ** n)
