# -*- coding: utf-8 -*-
"""usfm2osis._compat

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
import sys

# pylint: disable=invalid-name
if sys.version_info[0] == 3: # pragma: no cover
    _range = range
    _unicode = str
    _unichr = chr
else: # pragma: no cover
    _range = xrange
    _unicode = unicode
    _unichr = unichr
