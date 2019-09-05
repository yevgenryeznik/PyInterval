#!/usr/local/bin/python3
from PyInterval import Interval


class Box(object):
    # class constructor
    def __init__(self, low=0, upp=None):
        """
        :type low: List[int]
        :type low: List[float]
        :type upp: List[int]
        :type upp: List[float]
        :rtype: Box
        """
        if upp is None:
            upp = low
        if len(low) != len(upp):
            raise ValueError('The number of lower bounds is not the same as the number of upper bounds!')
        dim = len(low)
        self.size = [dim, 1]
        self.intervals = [Interval(low[d], upp[d]) for d in range(0, dim)]

    # overloading indexing operator
    def __getitem__(self, index):
        return self.intervals[index]

    # string representation of the box
    def __str__(self):
        box_to_print = ""
        for d in range(0, self.size[0]):
            box_to_print += self.intervals[d].__str__()  # +"\n"

        return box_to_print

    # addition operator overloading
    def __add__(self, other):
        dim = self.size[0]
        if isinstance(other, (int, float)):
            other = Box([other]*dim)

        result = Box([0]*dim)
        result.intervals = [self.intervals[d] + other.intervals[d] for d in range(0, dim)]
        return result

    # addition operator overloading (used in the case 'number' + 'box' by converting 'number' to 'box')
    def __radd__(self, other):
        dim = self.size[0]
        if isinstance(other, (int, float)):
            other = Box([other]*dim)

        result = Box([0]*dim)
        result.intervals = [other.intervals[d] + self.intervals[d] for d in range(0, dim)]
        return result

    # subtraction operator overloading
    def __sub__(self, other):
        dim = self.size[0]
        if isinstance(other, (int, float)):
            other = Box([other]*dim)

        result = Box([0]*dim)
        result.intervals = [self.intervals[d] - other.intervals[d] for d in range(0, dim)]
        return result

    # subtraction operator overloading (used in the case 'number' - 'box' by converting 'number' to 'box')
    def __rsub__(self, other):
        dim = self.size[0]
        if isinstance(other, (int, float)):
            other = Box([other]*dim)

        result = Box([0]*dim)
        result.intervals = [other.intervals[d] - self.intervals[d] for d in range(0, dim)]
        return result

    # multiplication operator overloading
    def __mul__(self, other):
        dim = self.size[0]
        if isinstance(other, (int, float)):
            other = Box([other]*dim)
        elif isinstance(other, Interval):
            other = Box([other.low]*dim, [other.upp] * dim)
        result = Box([0]*dim)
        result.intervals = [self.intervals[d]*other.intervals[d] for d in range(0, dim)]
        return result

    # multiplication operator overloading (used in the case 'number' * 'box' by converting 'number' to 'box')
    def __rmul__(self, other):
        dim = self.size[0]
        if isinstance(other, (int, float)):
            other = Box([other]*dim)
        elif isinstance(other, Interval):
            other = Box([other.low]*dim, [other.upp]*dim)
        return other.__mul__(self)

    # division operator overloading
    def __div__(self, other):
        dim = self.size[0]
        if isinstance(other, (int, float)):
            other = Box([other]*dim)

        if any([0 <= item for item in other.intervals]):
            raise ValueError('Impossible operation: division by the box which contains zero(s) along its dimension(s)')
        else:
            result = Box([0]*dim)
            result.intervals = [self.intervals[d]/other.intervals[d] for d in range(0, dim)]
            return result

    # division operator overloading (used in the case 'number' / 'box' by converting 'number' to 'box')
    def __rdiv__(self, other):
        dim = self.size[0]
        if isinstance(other, (int, float)):
            other = Box([other]*dim)
        elif isinstance(other, Interval):
            other = Box([other.low]*dim, [other.upp]*dim)
        return other.__div__(self)

    # unary minus operator overloading
    def __pos__(self):
        return self

    # unary minus operator overloading
    def __neg__(self):
        dim = self.size[0]
        result = Box([0]*dim)
        result.intervals = [-item for item in self.intervals]
        return result

    # equal operator "==" operator overloading
    def __eq__(self, other):
        dim = self.size[0]
        if isinstance(other, (int, float)):
            other = Box([other]*dim)
        result = all([self.intervals[d] == other.intervals[d] for d in range(0, dim)])
        return result

    # not equal operator "!=" operator overloading
    def __ne__(self, other):
        dim = self.size[0]
        if isinstance(other, (int, float)):
            other = Box([other]*dim)

        result = any([self.intervals[d] != other.intervals[d] for d in range(0, dim)])
        return result

    # less or  equal operator "<=" overloading. Means " self inside other"
    def __le__(self, other):
        dim = self.size[0]
        if isinstance(other, (int, float)):
            other = Box([other]*dim)

        result = all([self.intervals[d] <= other.intervals[d] for d in range(0, dim)])
        return result

    # less than operator "<" overloading. Means " self inside int(other)"
    def __lt__(self, other):
        dim = self.size[0]
        if isinstance(other, (int, float)):
            other = Box([other]*dim)

        result = all([self.intervals[d] < other.intervals[d] for d in range(0, dim)])
        return result

    # greater or  equal operator ">=" overloading. Means " other inside self"
    def __ge__(self, other):
        dim = self.size[0]
        if isinstance(other, (int, float)):
            other = Box([other]*dim)

        result = all([self.intervals[d] >= other.intervals[d] for d in range(0, dim)])
        return result

    # less than operator ">" overloading. Means " other inside int(self)"
    def __gt__(self, other):
        dim = self.size[0]
        if isinstance(other, (int, float)):
            other = Box([other]*dim)

        result = all([self.intervals[d] > other.intervals[d] for d in range(0, dim)])
        return result

    # overloading | operator. Means  hull of two intervals
    def __or__(self, other):
        dim = self.size[0]
        if isinstance(other, (int, float)):
            other = Box([other]*dim)
        result = Box([0]*dim)
        result.intervals = [self.intervals[d] | other.intervals[d] for d in range(0, dim)]
        return result

    # overloading & operator. Means  intersection of two intervals
    def __and__(self, other):
        dim = self.size[0]
        if isinstance(other, (int, float)):
            other = Box([other]*dim)
        result = Box([0]*dim)
        result.intervals = [self.intervals[d] & other.intervals[d] for d in range(0, dim)]
        return result

    # overloading operator ** . Means self in the power of other (other is a number)
    def __pow__(self, other):
        dim = self.size[0]
        result = Box([0]*dim)
        result.intervals = [self.intervals[d]**other for d in range(0, dim)]
        return result

    # overloading operator ** . Means other in the power of self (other is a number)
    def __rpow__(self, other):
        dim = self.size[0]
        result = Box([0]*dim)
        result.intervals = [other**self.intervals[d] for d in range(0, dim)]
        return result

    def __abs__(self):
        dim = self.size[0]
        result = Box([0]*dim)
        result.intervals = [abs(self.intervals[d]) for d in range(0, dim)]
        return result
