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


class Kind(object):
    """Type to handle primitive objects (not collections, eg: None, int, str) as a functors"""
    def __new__(cls, wrap):
        if isinstance(wrap, Kind):
            return wrap
        obj = super(Kind, cls).__new__(cls)
        obj.__init(wrap)
        return obj

    def __init(self, wrap):
        self.wrap = wrap

    def __nonzero__(self):
        """test if object is True or False"""
        return bool(self.wrap)

    def __or__(self, other):
        """ operator |
        >>> Kind(0) | None | '' | 0  > 1
        ''         # 4 constructors of Kind is called
        >>> Kind(0) | 100 | None | True  > 1
        100        # only two Kind constructor is called (Kind(0) and Kind(None))
        >>> Kind(0) | 100 | Kind(None) | Kind(True)  > 1
        100        # for Kind constructor is called
        """
        if self.wrap: return self
        else: return Kind(other)

    def __gt__(self, tmp):
        """ operator >  -- performs extract value
        operator > needs additional operand, which can be anything"""
        return self.wrap

    def fmap(self, f):
        if self.wrap is not None:
            self.wrap = f(self.wrap)
        return self
