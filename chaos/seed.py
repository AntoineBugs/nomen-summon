from math import sin
from datetime import datetime, date


def date_diff(ref:date, y:int, m:int, d:int):
    dt = datetime(y, m, d)
    diff = dt.date() - ref
    return diff.days


def shift_float(f, ref:date):
    return lambda y, m, d: f(date_diff(ref, y, m, d))


def sin_shift(ref:date):
    f = lambda x: (sin(x)+1)/2
    return shift_float(f, ref)


def get_functions(ref):
    d = {'date_diff': lambda y, m, d: date_diff(ref, y, m, d)}
    d.update({'shift_float': lambda f: shift_float(f, ref)})
    d.update({'sin_shift': sin_shift(ref)})
    return d