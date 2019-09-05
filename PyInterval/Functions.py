#!/usr/local/bin/python3
import numpy as np

import Rounding
from PyInterval import Interval, Box


# elementary functions defined for an argument of the types Interval and Box
class Function(object):
    # constructor of a class
    def __init__(self, fun, *args):
        """
         :type fun: Callable
         :rtype: Function
         """
        self.fun = fun

        # processing additional parameter (base) for logarithmic function
        if fun == np.log:
            if args:
                if len(args) > 1:
                    raise ValueError('Too much input arguments for logarithmic function')
                else:
                    base = args.__getitem__(0)
                    if (base <= 0) | (base == 1):
                        raise ValueError('Logarithm base must be either in (0, 1) or greater than 1')
                    else:
                        self.base = base
            else:
                self.base = np.exp(1)

    # make class Function callable
    def __call__(self, x):
        fun = self.fun
        if isinstance(x, (int, float)):
            return fun(x)
        elif isinstance(x, (list, np.ndarray)):
            if all([isinstance(item, (int, float)) for item in x]):
                x = Box(x)
                return self.__call__(x)
        elif isinstance(x, Interval):
            result = Interval(0)

            # square root function
            if fun == np.sqrt:
                result = x**0.5

            # exponential function
            elif fun == np.exp:
                Rounding.setRoundDown()
                result.low = fun(x.low)

                Rounding.setRoundUp()
                result.upp = fun(x.upp)

            # logarithmic function
            elif fun == np.log:
                base = self.base
                if x.low <= 0:
                    raise ValueError('Lower bound of interval must be > 0')
                Rounding.setRoundDown()
                result.low = (((0 < base) & (base < 1))*fun(x.upp) + (base > 1)*fun(x.low))/fun(base)

                Rounding.setRoundUp()
                result.upp = (((0 < base) & (base < 1))*fun(x.low) + (base > 1)*fun(x.upp))/fun(base)

            # sin function
            elif fun == np.sin:
                # check if a set {2pi*k + 0.5pi, k in Z} has non-empty intersection with x
                s1 = (np.ceil((x.low + 0.5*np.pi)/(2*np.pi)) <= np.floor((x.upp + 0.5*np.pi)/(2*np.pi)))

                # check if a set {2pi*k - 0.5pi, k in Z} has non-empty intersection with x
                s2 = (np.ceil((x.low - 0.5*np.pi)/(2*np.pi)) <= np.floor((x.upp - 0.5*np.pi)/(2*np.pi)))

                if s1 & s2:
                    Rounding.setRoundDown()
                    result.low = -1.0

                    Rounding.setRoundUp()
                    result.upp = 1.0

                elif s1 & (not s2):
                    Rounding.setRoundDown()
                    result.low = -1.0

                    Rounding.setRoundUp()
                    result.upp = np.max(fun([x.low, x.upp]))

                elif (not s1) & s2:
                    Rounding.setRoundDown()
                    result.low = np.min(fun([x.low, x.upp]))

                    Rounding.setRoundUp()
                    result.upp = 1.0
                else:
                    Rounding.setRoundDown()
                    result.low = np.min(fun([x.low, x.upp]))

                    Rounding.setRoundUp()
                    result.upp = np.max(fun([x.low, x.upp]))

            # asin function
            elif fun == np.arcsin:
                if x.low < -1:
                    raise ValueError('Lower bound of interval must be >= -1')

                elif x.upp > 1:
                    raise ValueError('Upper bound of interval must be <= 1')

                else:
                    Rounding.setRoundDown()
                    result.low = fun(x.low)

                    Rounding.setRoundUp()
                    result.upp = fun(x.upp)

            # atan function
            elif fun == np.arctan:
                Rounding.setRoundDown()
                result.low = fun(x.low)

                Rounding.setRoundUp()
                result.upp = fun(x.upp)

            Rounding.setRoundNear()
            return result

        elif isinstance(x, Box):
            result = Box([0] * x.size[0])
            result.intervals = [self.__call__(x[d]) for d in range(0, x.size[0])]
            return result

        else:
            raise TypeError('Input must be either number or interval, or box')


# square root function
def sqrt(x):
    fcn = Function(np.sqrt)
    return fcn(x)


# exponential function
def exp(x):
    fcn = Function(np.exp)
    return fcn(x)


# logarithmic function
def log(x, base=np.exp(1)):
    fcn = Function(np.log, base)
    return fcn(x)


# trigonometric functions: sin
def sin(x):
    fcn = Function(np.sin)
    return fcn(x)


# trigonometric functions: cos
def cos(x):
    fcn = Function(np.sin)
    return fcn(x + 0.5*np.pi)


# trigonometric functions: tan
def tan(x):
    return sin(x)/cos(x)


# hyperbolic functions: sinh
def sinh(x):
    return 0.5*(exp(x) - exp(-x))


# hyperbolic functions: cosh
def cosh(x):
    return 0.5*(exp(x) + exp(-x))


# hyperbolic functions: tanh
def tanh(x):
    return sinh(x)/cosh(x)


# inverse trigonometric functions: asin
def asin(x):
    fcn = Function(np.arcsin)
    return fcn(x)


# inverse trigonometric functions: acos
def acos(x):
    fcn = Function(np.arcsin)
    return 0.5*np.pi - fcn(x)


# inverse trigonometric functions: atan
def atan(x):
    fcn = Function(np.arctan)
    return fcn(x)
