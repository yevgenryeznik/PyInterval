#!/usr/local/bin/python3

import Interval


def midpoint(fun, low, upp, tol=1e-3):
    result = (upp-low)*fun(Interval.Interval(low, upp))
    if 2*result.rad < tol:
        return result
    else:
        mid = 0.5 * (low + upp)
        return midpoint(fun, low, mid, tol/2.0)+midpoint(fun, mid, upp, tol/2.0)


