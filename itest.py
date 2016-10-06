#!/usr/bin/python
from interval import *
from box import *
from functions import *

a = Interval(2, 3)
print 3+a
print a + 3
print "------"
print(Interval(1.0)/10)
print sqrt(Interval(2, 3))
print sqrt(Box([2], [3]))
print exp(Interval(2, 3))
print log(Interval(2, 32))
print log(Interval(2, 32), 4)
print sin(Interval(5, 6))
print cos(Interval(5, 6))
print tan(Interval(5, 6))
print sinh(Interval(1, 2))
print cosh(Interval(1, 2))
print tanh(Interval(1, 2))
print asin(Interval(-1, 1))
print acos(Interval(-1, 1))
print atan(Interval(-10000, 10000))
print "atan(Box([-1000]*2, [10000]*2)) = "
print atan(Box([-1000]*2, [10000]*2))
