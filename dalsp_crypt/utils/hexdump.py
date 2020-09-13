# -*- coding:utf-8 -*-
#
# Copyright (C) 2015 Carlos Jenkins <carlos@jenkins.co.cr>
#
# This program is free software: you can redistribute it and/or modify
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Hexdump implementation in Python 2.7 and 3.
"""

from __future__ import unicode_literals

import sys

__python3__ = sys.version_info > (3,)


def ordp(c):
    """
    Helper that returns a printable binary data representation.
    """
    output = []

    if __python3__:
        for i in c:
            if (i < 32) or (i >= 127):
                output.append('.')
            else:
                output.append(chr(i))
    else:
        for i in c:
            j = ord(i)
            if (j < 32) or (j >= 127):
                output.append('.')
            else:
                output.append(i)

    return ''.join(output)


def hexdump(p):
    """
    Return a hexdump representation of binary data.

    Usage:

    >>> from hexdump import hexdump
    >>> print(hexdump(
    ...     b'\\x00\\x01\\x43\\x41\\x46\\x45\\x43\\x41\\x46\\x45\\x00\\x01'
    ... ))
    0000   00 01 43 41 46 45 43 41  46 45 00 01               ..CAFECAFE..
    """
    output = []
    l = len(p)
    i = 0
    while i < l:
        output.append('{:04d}   '.format(i))
        for j in range(16):
            if (i + j) < l:
                if __python3__:
                    byte = p[i + j]
                else:
                    byte = ord(p[i + j])
                output.append('{:02X} '.format(byte))
            else:
                output.append('   ')
            if (j % 16) == 7:
                output.append(' ')
        output.append('  ')
        output.append(ordp(p[i:i + 16]))
        output.append('\n')
        i += 16
    return ''.join(output)


__all__ = ['hexdump']
