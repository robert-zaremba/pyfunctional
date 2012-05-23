from functional import *


def test_curry():
    @curry
    def f(arg1, arg2, arg3='defult'):
        return arg1+arg2+arg3

    f1 = f('a', arg3=' other')
    assert isinstance(f1, curry)
    assert f1('b') == 'ab other'


def test_curry2():
    def f(arg1, arg2, arg3='defult'):
        return arg1+arg2+arg3

    fc = curry(f, 'a')
    fc2 = fc(arg3=' other')
    x = fc2('b')                        # returns 'ab other'
    assert isinstance(fc2, curry)
    assert x == 'ab other'
