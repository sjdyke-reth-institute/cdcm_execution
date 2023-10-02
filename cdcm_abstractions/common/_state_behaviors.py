"""Patterns describing common behavior of `State` nodes

Author:
    R Murali Krishnan
    
Date:
    09.18.2023
    
"""


__all__ = ["polynominal", "linear_function", "product"]

from cdcm import clip
import operator as op
from numbers import Number
from functools import partial, reduce


def polynominal(order: int, _clip: bool=True, lval: Number=0.0, uval: Number=1.0):
    """A polynominal function"""
    def f(state, dt, rate, *args, **kwargs):
        rate_term = [rate ** i for i in range(1, order + 1)]
        new_state = state - dt * sum(rate_term)
        return clip(new_state, lval, uval) if _clip else new_state
    return f


linear_function = partial(polynominal, order=1)

def product(*args):
    """Product of all arguments"""
    return reduce(op.mul, args, 1)