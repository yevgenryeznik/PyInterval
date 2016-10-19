#!/usr/bin/python

import interval
import functions as fcn


def midpoint(fun, low, upp, tol=1e-3):
    result = (upp-low)*fun(interval.Interval(low, upp))
    if 2*result.rad < tol:
        return result
    else:
        mid = 0.5 * (low + upp)
        return midpoint(fun, low, mid, tol/2.0)+midpoint(fun, mid, upp, tol/2.0)


def fun(x):
    return fcn.sin(fcn.cos(fcn.exp(x)))

a, b = 2, 5
integral_value = midpoint(fun, -2, 2)

print integral_value, " ", 2*integral_value.rad