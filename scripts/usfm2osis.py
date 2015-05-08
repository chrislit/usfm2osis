#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""usfm2osis.py
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

 ----------------------------

 Guidelines & objectives:
 *Target CPython 2.6+ and 3.2+, plus PyPy
 *Require no non-default libraries
 *Handle all USFM characters from the USFM reference:
      <http://paratext.org/about/usfm>
 *Employ best-practice conformant OSIS
 *Employ modularity (functions rather than a big long script)
 *Employ the same command-line syntax as usfm2osis.pl
 *Use non-characters for milestoning (internally only)
"""
from __future__ import print_function, unicode_literals, absolute_import

#date = '$Date: 2014-02-22 23:59:38 -0800 (Sat, 22 Feb 2014) $'
#rev = '$Rev: 480 $'

usfmVersion = '2.35'  # http://ubs-icap.org/chm/usfm/2.35/index.html
osisVersion = '2.1.1' # http://www.bibletechnologies.net/osisCore.2.1.1.xsd
scriptVersion = '0.6.1'

### Key to non-characters:
# Used   : \uFDD0\uFDD1\uFDD2\uFDD3\uFDD4\uFDD5\uFDD6\uFDD7\uFDD8\uFDD9\uFDDA
#          \uFDDB\uFDDC\uFDDD\uFDDE\uFDDF\uFDE0\uFDE1\uFDE2\uFDE3\uFDE4\uFDE5
#          \uFDE6
# Unused : \uFDE7\uFDE8\uFDE9\uFDEA\uFDEB\uFDEC\uFDED\uFDEE\uFDEF
# \uFDD0 book
# \uFDD1 chapter
# \uFDD2 verse
# \uFDD3 paragraph
# \uFDD4 title
# \uFDD5 ms1
# \uFDD6 ms2
# \uFDD7 ms3
# \uFDD8 ms4
# \uFDD9 ms5
# \uFDDA s1
# \uFDDB s2
# \uFDDC s3
# \uFDDD s4
# \uFDDE s5
# \uFDDF notes
# \uFDE0 intro-list
# \uFDE1 intro-outline
# \uFDE2 is1
# \uFDE3 is2
# \uFDE4 is3
# \uFDE5 is4
# \uFDE6 is5
# \uFDD5\uFDD6\uFDD7\uFDD8\uFDD9\uFDDA\uFDDB\uFDDC\uFDDD\uFDDE sections

import multiprocessing
import random
import sys
import re
import codecs
from encodings.aliases import aliases

sys.path = sys.path[1:]
from usfm2osis.util import verbosePrint
from usfm2osis.convert import convertToOsis, osisSchema
from usfm2osis.bookdata import bookDict, addBookDict, filename2osis
from usfm2osis.sort import keynat, keycanon, keyusfm, keysupplied

# pylint: disable=invalid-name
if sys.version_info[0] == 3: # pragma: no cover
    _range = range
    import queue as Queue
else: # pragma: no cover
    _range = xrange
    import Queue


#date = date.replace('$', '').strip()[6:16]
#rev = rev.replace('$', '').strip()[5:]

osis2locBk = dict()
loc2osisBk = dict()
#filename2osis = dict()
verbose = bool()
ucs4 = (sys.maxunicode > 0xFFFF)

relaxedConformance = False
encoding = ''
debug = False
verbose = False

def readIdentifiersFromOsis(filename):
    """Reads the USFM file and stores information about which Bible book it
    represents and localized abbrevations in global variables.

    Keyword arguments:
    filename -- a USFM filename

    """

    global encoding
    global loc2osisBk, osis2locBk

    ### Processing starts here
    if encoding:
        osis = codecs.open(filename, 'r', encoding).read().strip() + '\n'
    else:
        encoding = 'utf-8'
        osis = codecs.open(filename, 'r', encoding).read().strip() + '\n'
        # \ide_<ENCODING>
        encoding = re.search(r'\\ide\s+(.+)'+'\n', osis)
        if encoding:
            encoding = encoding.group(1).lower().strip()
            if encoding != 'utf-8':
                if encoding in aliases:
                    osis = codecs.open(filename, 'r', encoding).read().strip() + '\n'
                else:
                    #print(('WARNING: Encoding "' + encoding + '" unknown, processing ' + filename + ' as UTF-8'))
                    encoding = 'utf-8'

    # keep a copy of the OSIS book abbreviation for below (\toc3 processing) to store for mapping localized book names to/from OSIS
    osisBook = re.search(r'\\id\s+([A-Z0-9]+)', osis)
    if osisBook:
        osisBook = bookDict[osisBook.group(1)]
        filename2osis[filename] = osisBook

    locBook = re.search(r'\\toc3\b\s+(.+)\s*'+'\n', osis)
    if locBook:
        locBook = locBook.group(1)
        if osisBook:
            osis2locBk[osisBook]=locBook
            loc2osisBk[locBook]=osisBook


def printUsage():
    """Prints usage statement."""
    print(('usfm2osis.py -- USFM ' + usfmVersion + ' to OSIS ' + osisVersion + ' converter version ' + scriptVersion))
    #    print(('                Revision: ' + rev + ' (' + date + ')'))
    print('')
    print('Usage: usfm2osis.py <osisWork> [OPTION] ...  <USFM filename|wildcard> ...')
    print('')
    print('  -d               debug mode (single-threaded, verbose output)')
    print('  -e ENCODING      input encoding override (default is to read the USFM file\'s')
    print('                     \\ide value or assume UTF-8 encoding in its absence)')
    print('  -h, --help       print this usage information')
    print('  -o FILENAME      output filename (default is: <osisWork>.osis.xml)')
    print('  -r               enable relaxed markup processing (for non-standard USFM)')
    print('  -s mode          set book sorting mode: natural (default), alpha, canonical,')
    print('                     usfm, random, none')
    print('  -v               verbose feedback')
    print('  -x               disable XML validation')
    print('')
    print('As an example, if you want to generate the osisWork <Bible.KJV> and your USFM')
    print('  are located in the ./KJV folder, enter:')
    print('    python usfm2osis.py Bible.KJV ./KJV/*.usfm')
    verbosePrint('', verbose)
    verbosePrint('Supported encodings: ' + ', '.join(aliases), verbose)


class Worker(multiprocessing.Process):
    """Worker object for multiprocessing."""
    def __init__(self, work_queue, result_queue):
        # base class initialization
        multiprocessing.Process.__init__(self)

        # job management stuff
        self.work_queue = work_queue
        self.result_queue = result_queue
        self.kill_received = False

    def run(self):
        while not self.kill_received:
            # get a task
            try:
                job = self.work_queue.get_nowait()
            except Queue.Empty:
                break

            # the actual processing
            osis = convertToOsis(job, relaxedConformance, encoding, debug, verbose)
            # TODO: move XML validation here?

            # store the result
            self.result_queue.put((job,osis))



if __name__ == "__main__":
    num_processes = max(1,multiprocessing.cpu_count()-1)
    num_jobs = num_processes

    encoding = ''
    relaxedConformance = False
    inputFilesIdx = 2 # This marks the point in the sys.argv array, after which all values represent USFM files to be converted.
    usfmDocList = list()

    if '-v' in sys.argv:
        verbose = True
        inputFilesIdx += 1
    else:
        verbose = False

    if '-x' in sys.argv:
        validatexml = False
        inputFilesIdx += 1
    else:
        validatexml = True

    if '-d' in sys.argv:
        debug = True
        inputFilesIdx += 1
        num_processes = 1
        num_jobs = 1
        verbose = True
    else:
        debug = False

    if '-h' in sys.argv or '--help' in sys.argv or len(sys.argv) < 3:
        printUsage()
    else:
        osisWork = sys.argv[1]

        if '-o' in sys.argv:
            i = sys.argv.index('-o')+1
            if len(sys.argv) < i+1:
                printUsage()
            osisFileName = sys.argv[i]
            inputFilesIdx += 2 # increment 2, reflecting 2 args for -o
        else:
            osisFileName = osisWork + '.osis.xml'

        if '-e' in sys.argv:
            i = sys.argv.index('-e')+1
            if len(sys.argv) < i+1:
                printUsage()
            encoding = sys.argv[i]
            inputFilesIdx += 2 # increment 2, reflecting 2 args for -e

        if '-r' in sys.argv:
            relaxedConformance = True
            bookDict = dict(list(bookDict.items()) + list(addBookDict.items()))
            inputFilesIdx += 1

        if '-s' in sys.argv:
            i = sys.argv.index('-s')+1
            if len(sys.argv) < i+1:
                printUsage()
            if sys.argv[i].startswith('a'):
                sortKey = None
                print('Sorting book files alphanumerically')
            elif sys.argv[i].startswith('na'):
                sortKey = keynat
                print('Sorting book files naturally')
            elif sys.argv[i].startswith('c'):
                sortKey = keycanon
                print('Sorting book files canonically')
            elif sys.argv[i].startswith('u'):
                sortKey = keyusfm
                print('Sorting book files by USFM book number')
            elif sys.argv[i].startswith('random'): # for testing only
                sortKey = lambda filename: int(random.random()*256)
                print('Sorting book files randomly')
            else:
                sortKey = keysupplied
                print('Leaving book files unsorted, in the order in which they were supplied')
            inputFilesIdx += 2 # increment 2, reflecting 2 args for -s
        else:
            sortKey = keynat
            print('Sorting book files naturally')

        usfmDocList = sys.argv[inputFilesIdx:]

        for filename in usfmDocList:
            readIdentifiersFromOsis(filename)
        usfmDocList = sorted(usfmDocList, key=sortKey)

        # run
        # load up work queue
        work_queue = multiprocessing.Queue()
        for job in usfmDocList:
            work_queue.put(job)

        # create a queue to pass to workers to store the results
        result_queue = multiprocessing.Queue()

        # spawn workers
        print('Converting USFM documents to OSIS...')
        for i in _range(num_processes):
            worker = Worker(work_queue, result_queue)
            worker.start()

        # collect the results off the queue
        osisSegment = dict()
        for i in usfmDocList:
            k,v=result_queue.get()
            osisSegment[k]=v

        print('Assembling OSIS document')
        osisDoc = '<osis xmlns="http://www.bibletechnologies.net/2003/OSIS/namespace" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.bibletechnologies.net/2003/OSIS/namespace http://www.bibletechnologies.net/osisCore.'+osisVersion+'.xsd">\n<osisText osisRefWork="Bible" xml:lang="und" osisIDWork="' + osisWork + '">\n<header>\n<work osisWork="' + osisWork + '"/>\n</header>\n'

        unhandledTags = set()
        for doc in usfmDocList:
            unhandledTags |= set(re.findall(r'(\\[^\s]*)', osisSegment[doc]))
            osisDoc += osisSegment[doc]

        osisDoc += '</osisText>\n</osis>\n'

        if validatexml:
            try:
                #import urllib
                from lxml import etree
                print('Validating XML...')
                osisParser = etree.XMLParser(schema = etree.XMLSchema(etree.XML(osisSchema)))
                #osisParser = etree.XMLParser(schema = etree.XMLSchema(etree.XML(urllib.urlopen('http://www.bibletechnologies.net/osisCore.' + osisVersion + '.xsd').read())))
                etree.fromstring(osisDoc, osisParser)
                print('XML Valid')
            except ImportError:
                print('For schema validation, install lxml')
            except etree.XMLSyntaxError as eVal:
                print('XML Validation error: ' + str(eVal))

        osisFile = codecs.open(osisFileName, 'w', 'utf-8')
        osisFile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        osisFile.write(osisDoc)

        print('Done!')

        if unhandledTags:
            print('')
            print(('Unhandled USFM tags: ' + ', '.join(sorted(unhandledTags)) + ' (' + str(len(unhandledTags)) + ' total)'))
            if not relaxedConformance:
                print('Consider using the -r option for relaxed markup processing')

