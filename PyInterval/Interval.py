#!/usr/bin/python
import numpy as np
import Rounding


class Interval(object):
    # class constructor
    def __init__(self, low=0, upp=None):
        """
        :type low: int
        :type low: float
        :type upp: int
        :type upp: float
        :rtype: Interval
        """
        if upp is None:
            upp = low
        if low > upp:
            raise ValueError('Lower value {low:f} is greater than upper value {upp:f}'.format(low=low, upp=upp))
        Rounding.setRoundDown()
        self.low = float(low)

        Rounding.setRoundUp()
        self.upp = float(upp)

        Rounding.setRoundNear()
        self.mid = 0.5 * (upp + low)
        self.rad = 0.5 * (upp - low)
        self.mig = (1 - (low <= 0 & 0 <= upp)) * np.min([np.abs(low), np.abs(upp)])
        self.mag = np.max([np.abs(low), np.abs(upp)])

    # string representation of the interval
    def __str__(self):
        return '[{low:.17f}, {upp:.17f}]\n'.format(low=self.low, upp=self.upp)

    # addition operator overloading
    def __add__(self, other):
        """
        :type other: int
        :type other: float
        :type other: Interval
        """
        if isinstance(other, (int, float)):
            other = Interval(float(other), float(other))

        Rounding.setRoundDown()
        low = self.low + other.low

        Rounding.setRoundUp()
        upp = self.upp + other.upp

        Rounding.setRoundNear()
        return Interval(low, upp)

    # addition operator overloading (used in the case 'number' + 'interval' by converting 'number' to 'interval')
    def __radd__(self, other):
        if isinstance(other, (int, float)):
            other = Interval(other, other)

        return other.__add__(self)

    # subtraction operator overloading
    def __sub__(self, other):
        if isinstance(other, (int, float)):
            other = Interval(other, other)

        Rounding.setRoundDown()
        low = self.low - other.upp

        Rounding.setRoundUp()
        upp = self.upp - other.low

        Rounding.setRoundNear()
        return Interval(low, upp)

    # subtraction operator overloading (used in the case 'number' - 'interval' by converting 'number' to 'interval')
    def __rsub__(self, other):
        if isinstance(other, (int, float)):
            other = Interval(other, other)

        return other.__sub__(self)

    # multiplication operator overloading
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            other = Interval(other, other)
        low1, upp1 = self.low, self.upp
        low2, upp2 = other.low, other.upp

        Rounding.setRoundDown()
        low = np.min([low1 * low2, low1 * upp2, upp1 * low2, upp1 * upp2])

        Rounding.setRoundUp()
        upp = np.max([low1 * low2, low1 * upp2, upp1 * low2, upp1 * upp2])

        Rounding.setRoundNear()
        return Interval(low, upp)

    # multiplication operator overloading (used in the case 'number' * 'interval' by converting 'number' to 'interval')
    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            other = Interval(other, other)

        return other.__mul__(self)

    # division operator overloading (self is in numerator)
    def __div__(self, other):
        if isinstance(other, (int, float)):
            other = Interval(other, other)

        if 0 <= other:
            raise ValueError('Impossible operation: division by the interval which contains zero')

        else:
            Rounding.setRoundDown()
            low = 1.0 / other.upp

            Rounding.setRoundUp()
            upp = 1.0 / other.low

            other = Interval(low, upp)
            Rounding.setRoundNear()

            return self.__mul__(other)

    # division operator overloading (self is in denominator)
    def __rdiv__(self, other):
        if isinstance(other, (int, float)):
            other = Interval(float(other), float(other))

        if 0 <= self:
            raise ValueError('Impossible operation: division by the interval which contains zero')

        else:
            return other.__div__(self)

    # unary plus operator overloading
    def __pos__(self):
        return self

    # unary minus operator overloading
    def __neg__(self):
        return Interval(-self.upp, -self.low)

    # equal operator "==" operator overloading
    def __eq__(self, other):
        if isinstance(other, (int, float)):
            other = Interval(other, other)

        return (self.low == other.low) & (self.upp == other.upp)

    # not equal operator "!=" operator overloading
    def __ne__(self, other):
        if isinstance(other, (int, float)):
            other = Interval(other, other)

        return (self.low != other.low) | (self.upp != other.upp)

    # less or  equal operator "<=" overloading. Means " self inside other"
    def __le__(self, other):
        if isinstance(other, (int, float)):
            other = Interval(other, other)
        return (other.low <= self.low) & (self.upp <= other.upp)

    # less than operator "<" overloading. Means " self inside int(other)"
    def __lt__(self, other):
        if isinstance(other, (int, float)):
            other = Interval(other, other)

        return (other.low < self.low) & (self.upp < other.upp)

    # greater or  equal operator ">=" overloading. Means " other inside self"
    def __ge__(self, other):
        if isinstance(other, (int, float)):
            other = Interval(other, other)

        return (self.low <= other.low) & (other.upp <= self.upp)

    # less than operator ">" overloading. Means " other inside int(self)"
    def __gt__(self, other):
        if isinstance(other, (int, float)):
            other = Interval(other, other)

        return (other.low < self.upp) & (self.upp < other.upp)

    # overloading | operator. Means  hull of two intervals
    def __or__(self, other):
        if isinstance(other, (int, float)):
            other = Interval(other, other)
        low = np.min([self.low, other.low])
        upp = np.max([self.upp, other.upp])
        return Interval(low, upp)

    # overloading & operator. Means  intersection of two intervals
    def __and__(self, other):
        if isinstance(other, (int, float)):
            other = Interval(other, other)
        if (self.upp < other.low) | (other.upp < self.low):
            return []
        else:
            low = np.max([self.low, other.low])
            upp = np.min([self.upp, other.upp])
            return Interval(low, upp)

    # overloading operator ** . Means self in the power of other (other is a number)
    def __pow__(self, other):
        if isinstance(other, int):
            if other < 0:
                if 0 <= self:
                    raise ValueError('Impossible operation: interval contains zero and power < 0')
                else:
                    low = (1.0/self.upp)**(-other)
                    upp = (1.0/self.low)**(-other)

            elif other > 0:
                if other % 2 != 0:
                    Rounding.setRoundDown()
                    low = self.low**other

                    Rounding.setRoundUp()
                    upp = self.upp**other

                else:
                    Rounding.setRoundDown()
                    low = self.mig**other

                    Rounding.setRoundUp()
                    upp = self.mag**other
            else:
                low = 1.0
                upp = 1.0

        elif isinstance(other, float):
            if self.low <= 0:
                raise ValueError('Lower bound of interval must be > 0')
            else:
                if other < 0:
                    low = (1.0/self.upp)**(-other)
                    upp = (1.0/self.low)**(-other)

                elif other > 0:
                    Rounding.setRoundDown()
                    low = self.low**other

                    Rounding.setRoundUp()
                    upp = self.upp**other

                else:
                    low = 1.0
                    upp = 1.0

        else:
            raise ValueError('The power value must be a number')

        Rounding.setRoundNear()
        return Interval(low, upp)

    # overloading operator ** . Means other in the power of self (other is a number)
    def __rpow__(self, other):
        if (other == 1) | (other <= 0):
            raise ValueError(
                'The base value is {0:f} but it must be either within interval (0, 1) or greater than 1'.format(other))
        else:
            if other > 1:
                Rounding.setRoundDown()
                low = other**self.low

                Rounding.setRoundUp()
                upp = other**self.upp
            else:
                Rounding.setRoundDown()
                low = other**self.upp

                Rounding.setRoundUp()
                upp = other**self.low

            Rounding.setRoundNear()
            return Interval(low, upp)

    def __abs__(self):
        return Interval(self.mig, self.mag)
