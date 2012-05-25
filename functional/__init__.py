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

__author__ = "Robert Zaremba"
__version__ = version = "0.5"
__license__ = 'GPLv3'


from functionrich import curry, FunctionRich, identity


def find_first(predicate, ls):
    """Returns first element of iterable ls conforming predicate"""
    for x in ls:
        if predicate(x):
            return x
    return None

