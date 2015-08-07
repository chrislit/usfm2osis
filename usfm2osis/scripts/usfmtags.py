#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""usfmtags

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

from __future__ import print_function, unicode_literals
import re
import sys
import codecs

USFM_VERSION = '2.35'  # http://ubs-icap.org/chm/usfm/2.35/index.html

SIMPLE_TAGS = frozenset(['\\id', '\\ide', '\\sts', '\\rem', '\\h', '\\toc1',
                         '\\toc2', '\\toc3', '\\ip', '\\ipi', '\\im', '\\imi',
                         '\\ipq', '\\imq', '\\ipr', '\\ib', '\\ili', '\\iot',
                         '\\ior', '\\ior*', '\\iex', '\\iqt', '\\iqt*',
                         '\\imte', '\\ie', '\\mr', '\\sr', '\\r', '\\rq',
                         '\\rq*', '\\d', '\\sp', '\\c', '\\ca', '\\ca*',
                         '\\cl', '\\cp', '\\cd', '\\v', '\\va', '\\va*',
                         '\\vp', '\\vp*', '\\p', '\\m', '\\pmo', '\\pm',
                         '\\pmc', '\\pmr', '\\mi', '\\nb', '\\cls', '\\pc',
                         '\\pr', '\\b', '\\qr', '\\qc', '\\qs', '\\qs*',
                         '\\qa', '\\qac', '\\qac*', '\\tr', '\\f', '\\f*',
                         '\\fe', '\\fe*', '\\fr', '\\fk', '\\fq', '\\fqa',
                         '\\fl', '\\fp', '\\fv', '\\ft', '\\fdc', '\\fdc*',
                         '\\fm', '\\fm*', '\\x', '\\x*', '\\xo', '\\xk',
                         '\\xq', '\\xt', '\\xot', '\\xot*', '\\xnt', '\\xnt*',
                         '\\xdc', '\\xdc*', '\\add', '\\add*', '\\bk', '\\bk*',
                         '\\dc', '\\dc*', '\\k', '\\k*', '\\lit', '\\nd',
                         '\\nd*', '\\ord', '\\ord*', '\\pn', '\\pn*', '\\qt',
                         '\\qt*', '\\sig', '\\sig*', '\\sls', '\\sls*', '\\tl',
                         '\\tl*', '\\wj', '\\wj*', '\\em', '\\em*', '\\bd',
                         '\\bd*', '\\it', '\\it*', '\\bdit', '\\bdit*', '\\no',
                         '\\no*', '\\sc', '\\sc*', '\\pb', '\\fig', '\\fig*',
                         '\\ndx', '\\ndx*', '\\pro', '\\pro*', '\\w', '\\w*',
                         '\\wg', '\\wg*', '\\wh', '\\wh*', '\\periph', '\\ef',
                         '\\ef*', '\\ex', '\\ex*', '\\esb', '\\esbe', '\\cat',
                         '\\z'])

DIGIT_TAGS = frozenset(['\\imt', '\\is', '\\iq', '\\io', '\\mt', '\\mte',
                        '\\ms', '\\s', '\\pi', '\\li', '\\ph', '\\q', '\\qm',
                        '\\th', '\\thr', '\\tc', '\\tcr'])


def main(args=None):
    tag_set = set()
    known_set = set()
    unknown_set = set()

    argv = sys.argv

    if '-h' in argv or '--help' in argv or len(argv) < 2:
        print_usage()
    else:
        for doc in argv[1:]:
            text = codecs.open(doc, 'r', 'utf-8').read()
            tag_set.update(set(re.findall(r'(\\[a-zA-Z0-9]+\b\*?)', text)))

        for tag in tag_set:
            if tag in SIMPLE_TAGS:
                known_set.add(tag)
            elif tag.rstrip('1234567890') in DIGIT_TAGS:
                known_set.add(tag)
            else:
                unknown_set.add(tag)

        print('Known USFM Tags: ' + ', '.join(sorted(known_set)))
        print('Unrecognized USFM Tags: ' + ', '.join(sorted(unknown_set)))


def print_usage():
    print('usfmtags <USFM filenames|wildcard>')
    print('')
    print(' This utility will scan USFM files and print two lists of all ' +
          'unique tags in\nthem.')
    print(' The first list identifies all valid tags, identified in the USFM ' +
          USFM_VERSION + ' spec.')
    print(' The second list identifies tags unknown to that spec.')
    exit()

if __name__ == "__main__":
    main()
