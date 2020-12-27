import os
from threading import Thread

data = [0, 0, 0]
clock = 0
width = 1600
height = 900
sep = os.path.sep

def map(x, in_min, in_max, out_min, out_max):
    """
    From https://www.arduino.cc/reference/en/language/functions/math/map/
    Re-maps a number from one range to another.
    That is, a value of fromLow would get mapped to toLow,
    a value of fromHigh to toHigh, values in-between to values in-between, etc.

    - value: the number to map.
    - fromLow: the lower bound of the value’s current range.
    - fromHigh: the upper bound of the value’s current range.
    - toLow: the lower bound of the value’s target range.
    - toHigh: the upper bound of the value’s target range.
    """
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def run_in_thread(func):
    thread = Thread(target=func)
    thread.daemon = True
    thread.start()