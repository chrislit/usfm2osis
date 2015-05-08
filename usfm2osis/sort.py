# -*- coding: utf-8 -*-
"""usfm2osis.sort

Copyright 2012-2015 by Christopher C. Little

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

The full text of the GNU General Public License is available at:
<http://www.gnu.org/licenses/gpl-3.0.txt>.
"""

from __future__ import unicode_literals
from .bookdata import canonicalOrder, usfmNumericOrder, filename2osis

# BEGIN PSF-licensed segment
# keynat from http://code.activestate.com/recipes/285264-natural-string-sorting/
def keynat(string):
    """A natural sort helper function for sort() and sorted() without using
    regular expressions or exceptions.

    >>> items = ('Z', 'a', '10th', '1st', '9')
    >>> sorted(items)
    ['10th', '1st', '9', 'Z', 'a']
    >>> sorted(items, key=keynat)
    ['1st', '9', '10th', 'a', 'Z']
    """
    it = type(1)
    r = []
    for c in string:
        if c.isdigit():
            d = int(c)
            if r and type( r[-1] ) == it:
                r[-1] = r[-1] * 10 + d
            else:
                r.append(d)
        else:
            r.append(c.lower())
    return r
# END PSF-licened segment

def keycanon(filename):
    """Sort helper function that orders according to canon position (defined in
    canonicalOrder list), returning canonical position or infinity if not in the
    list.

    """
    if filename in filename2osis:
        return canonicalOrder.index(filename2osis[filename])
    return float('inf')

def keyusfm(filename):
    """Sort helper function that orders according to USFM book number (defined
    in usfmNumericOrder list), returning USFM book number or infinity if not in
    the list.

    """
    if filename in filename2osis:
        return usfmNumericOrder.index(filename2osis[filename])
    return float('inf')

def keysupplied(filename):
    """Sort helper function that keeps the items in the order in which they were
    supplied (i.e. it doesn't sort at all), returning the number of times the
    function has been called.

    """
    if not hasattr(keysupplied, "counter"):
        keysupplied.counter = 0
    keysupplied.counter += 1
    return keysupplied.counter