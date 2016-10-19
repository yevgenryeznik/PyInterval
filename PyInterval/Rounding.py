#!/usr/bin/python

from sys import platform as _platform
from ctypes import cdll
from ctypes.util import find_library

lib_m = cdll.LoadLibrary(find_library('m'))

if _platform == "darwin":  # macOS
    ROUND_DOWN = 0x400
    ROUND_UP = 0x800
    ROUND_NEAR = 0

else:
    raise ImportError("Specify rounding mode constants for you platform")


def setRoundDown():
    lib_m.fesetround(ROUND_DOWN)


def setRoundUp():
    lib_m.fesetround(ROUND_UP)


def setRoundNear():
    lib_m.fesetround(ROUND_NEAR)
