# functional.py --- function composition in python
#
# Copyright 2010 Martin Wiebusch
# Copyright 2012 Robert Zaremba
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this module.  If not, see <http://www.gnu.org/licenses/>.


import inspect
import functools
from copy import copy

def _unpack(f, args):
    if isinstance(args, tuple):
        return f(*args)
    else:
        return f(args)



class curry(object):
    """make an callable object / function <f> in curry form (in terms of
    functional calculus).
    It behaves as normal partial, except the parital arguments
    are specified during function call
        @curry
        def f(arg1, arg2, arg3='defult'):
            return arg1+arg2+arg3

        f1 = f('a', arg3=' other')
        f1('b')                         # returns 'ab other'

    curry can behaves like functools.partial:
        def f(arg1, arg2, arg3='defult'):
            return arg1+arg2+arg3

        fc = curry(f, 'a')
        fc2 = fc(arg3='other')
        fc2('b')                        # returns 'ab other'
    """
    def __init__(self, f, *args, **kwargs):
        self.f = f
        self.f_spec = inspect.getargspec(f)
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        args_n  = self.args + args
        if self.kwargs:
            kwargs_n = self.kwargs.copy()
            kwargs_n.update(kwargs)
        else:
            kwargs_n = kwargs

        try:
            return self.f(*args_n, **kwargs_n)
        except TypeError as e:
            print e
            f2 = curry(self.f)
            f2.args   = args_n
            f2.kwargs = kwargs_n
            return f2


class FunctionRich(object):
    """This class serves as a wrapper for functions, providing operations found in functional style (composition operator and pointfree style)
    """
    _func = None

    def __init__(self, f, *args):
        if args:
            f = functools.partial(f, *args)
        if isinstance(f, FunctionRich):
            self._func = f._func
        elif inspect.isroutine(f) or inspect.isclass(f) or isinstance(f, functools.partial):
            self._func = f
        else:
            self._func = (lambda *args: f)

    # string representations
    def __repr__(self):
        return "functional.ComposableFunction("+self._func.__repr__()+")"
    def __str__(self):
        return self._func.__str__()

    # calls
    def __call__(self, *args):
        return self._func(*args)

    def __and__(self, arg):
        if isinstance(arg, tuple):
            return self._func(*arg)
        return self._func(arg)

    # composition
    def __mod__(self, f):
        f = FunctionRich(f)._func
        return FunctionRich(lambda *args: _unpack(self._func, f(*args)))
    def __rmod__(self, f):
        f = FunctionRich(f)._func
        return FunctionRich(lambda *args: _unpack(f, self._func(*args)))
    def __floordiv__(self, f):
        f = FunctionRich(f)._func
        return FunctionRich(lambda *args: self._func(f(*args)))
    def __rfloordiv__(self, f):
        f = FunctionRich(f)._func
        return FunctionRich(lambda *args: f(self._func(*args)))
    __lshift__ = __floordiv__
    __rshift__ = __rfloordiv__
    def __xor__(self, n):
        if isinstance(n, int) and n > 0:
            f = self
            for i in range(n-1):
                f = self % f
            return f
        elif n == 0:
            return identity
        else:
            return NotImplemented

    # binary operations
    def __add__(self, f):
        f = FunctionRich(f)._func
        return FunctionRich(lambda *args: self._func(*args) + f(*args))
    def __radd__(self, f):
        f = FunctionRich(f)._func
        return FunctionRich(lambda *args: f(*args) + self._func(*args))
    def __sub__(self, f):
        f = FunctionRich(f)._func
        return FunctionRich(lambda *args: self._func(*args) - f(*args))
    def __rsub__(self, f):
        f = FunctionRich(f)._func
        return FunctionRich(lambda *args: f(*args) - self._func(*args))
    def __mul__(self, f):
        f = FunctionRich(f)._func
        return FunctionRich(lambda *args: self._func(*args) * f(*args))
    def __rmul__(self, f):
        f = FunctionRich(f)._func
        return FunctionRich(lambda *args: f(*args) * self._func(*args))
    def __div__(self, f):
        f = FunctionRich(f)._func
        return FunctionRich(lambda *args: self._func(*args) / f(*args))
    def __rdiv__(self, f):
        f = FunctionRich(f)._func
        return FunctionRich(lambda *args: f(*args) / self._func(*args))

    # unary operations
    def __pow__(self, n):
        return FunctionRich(lambda *args: self._func(*args)**n)
    def __neg__(self):
        return FunctionRich(lambda *args: -self._func(*args))
    def __pos__(self):
        return self
    def __abs__(self):
        return FunctionRich(lambda *args: abs(self._func(*args)))

    # comparisons
    def __lt__(self, f):
        f = FunctionRich(f)._func
        return FunctionRich(lambda *args: self._func(*args) < f(*args))
    def __le__(self, f):
        f = FunctionRich(f)._func
        return FunctionRich(lambda *args: self._func(*args) <= f(*args))
    def __eq__(self, f):
        f = FunctionRich(f)._func
        return FunctionRich(lambda *args: self._func(*args) == f(*args))
    def __ne__(self, f):
        f = FunctionRich(f)._func
        return FunctionRich(lambda *args: self._func(*args) != f(*args))
    def __ge__(self, f):
        f = FunctionRich(f)._func
        return FunctionRich(lambda *args: self._func(*args) >= f(*args))
    def __gt__(self, f):
        f = FunctionRich(f)._func
        return FunctionRich(lambda *args: self._func(*args) > f(*args))



@FunctionRich
def identity(x):
    return x
