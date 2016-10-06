#!/usr/bin/python
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.patches import Rectangle
from functions import *
from interval import *
from box import *

rcParams['toolbar'] = 'None'


def plot(x, fun, beans=20, rectcol="lightblue", linecol="black", linewd=1.5):
    xlow = []
    for d in range(0, beans):
        xlow.append(x.low + 2 * x.rad / beans * d)
    xupp = [x.low + 2 * x.rad / beans * (d + 1) for d in range(0, beans)]
    xbox = Box(xlow, xupp)
    ybox = fun(xbox)

    fig = plt.figure()
    fig.set_facecolor("white")

    ax = fig.add_subplot(111)
    for d in range(0, beans):
        width = 2 * xbox[d].rad
        height = 2 * ybox[d].rad
        rect = Rectangle((xbox[d].low, ybox[d].low), width, height, fc=rectcol, visible=True)
        ax.add_patch(rect)
    xx = [xlow[0]] + xupp
    ax.plot(xx, [fun(xx[d]) for d in range(0, len(xx))], color=linecol, linewidth=linewd)
    ax.grid(True)
    plt.title(r"$\exp\left(-\frac{x^2}{10}\right)*(\cos(x) + \sin(\log(x)))$")
    plt.show()


def fcn(x):
    return exp(-x * x / 10) * (cos(x) + sin(log(x)))


x = Interval(0.1, 4)
plot(x, fcn, beans=100, linewd=2)
