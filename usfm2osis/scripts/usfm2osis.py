#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""usfm2osis
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

import multiprocessing
import random
import sys
import re
import codecs
import os
import pkgutil
from encodings.aliases import aliases

# sys.path = sys.path[1:]
from usfm2osis.util import verbose_print
from usfm2osis.convert import ConvertToOSIS
from usfm2osis.bookdata import BOOK_DICT, ADD_BOOK_DICT, FILENAME_TO_OSIS
from usfm2osis.sort import key_natural, key_canon, key_usfm, key_supplied

import usfm2osis

# pylint: disable=invalid-name
if sys.version_info[0] == 3:  # pragma: no cover
    _range = range
    import queue as Queue
else:  # pragma: no cover
    _range = xrange
    import Queue

usfmVersion = '2.35'  # http://ubs-icap.org/chm/usfm/2.35/index.html
osisVersion = '2.1.1'  # http://www.bibletechnologies.net/osisCore.2.1.1.xsd
scriptVersion = '0.6.1'

# -- Key to non-characters:
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

osis_to_loc_book = dict()
loc_to_osis_book = dict()
# filename2osis = dict()
verbose = bool()
ucs4 = (sys.maxunicode > 0xFFFF)

relaxed_conformance = False
encoding = ''
debug = False
verbose = False


def read_identifiers_from_osis(filename):
    """Reads the USFM file and stores information about which Bible book it
    represents and localized abbreviations in global variables.

    Keyword arguments:
    filename -- a USFM filename
    """
    global encoding
    global loc_to_osis_book, osis_to_loc_book

    #  Processing starts here
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
                    osis = codecs.open(filename, 'r',
                                       encoding).read().strip() + '\n'
                else:
                    # print(('WARNING: Encoding "' + encoding +
                    #       '" unknown, processing ' + filename + ' as UTF-8'))
                    encoding = 'utf-8'

    # keep a copy of the OSIS book abbreviation for below (\toc3 processing)
    # to store for mapping localized book names to/from OSIS
    osis_book = re.search(r'\\id\s+([A-Z0-9]+)', osis)
    if osis_book:
        osis_book = BOOK_DICT[osis_book.group(1)]
        FILENAME_TO_OSIS[filename] = osis_book

    loc_book = re.search(r'\\toc3\b\s+(.+)\s*' + '\n', osis)
    if loc_book:
        loc_book = loc_book.group(1)
        if osis_book:
            osis_to_loc_book[osis_book] = loc_book
            loc_to_osis_book[loc_book] = osis_book


def print_usage():
    """Prints usage statement."""
    print(('usfm2osis -- USFM ' + usfmVersion + ' to OSIS ' + osisVersion + ' converter version ' + scriptVersion))
    print('')
    print('Usage: usfm2osis <osisWork> [OPTION] ...  <USFM filename|wildcard> ...')
    print('')
    print('  -h, --help       print this usage information')
    print('  -d               debug mode (single-threaded, verbose output)')
    print('  -e ENCODING      input encoding override (default is to read the USFM file\'s')
    print('                     \\ide value or assume UTF-8 encoding in its absence)')
    print('  -o FILENAME      output filename (default is: <osisWork>.osis.xml)')
    print('  -r               enable relaxed markup processing (for non-standard USFM)')
    print('  -s MODE          set book sorting mode: natural (default), alpha, canonical,')
    print('                     usfm, random, none')
    print('  -t NUM           set the number of separate processes to use (your maximum')
    print('                     thread count by default)')
    print('  -l LANG          set the language value to a BCP 47 code (\'und\' by default)')
    print('  -v               verbose feedback')
    print('  -x               disable XML validation')
    print('')
    print('As an example, if you want to generate the osisWork <Bible.KJV> and your USFM')
    print('  are located in the ./KJV folder, enter:')
    print('    python usfm2osis Bible.KJV ./KJV/*.usfm')
    verbose_print('', verbose)
    verbose_print('Supported encodings: ' + ', '.join(aliases), verbose)


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
            osis = ConvertToOSIS(job, relaxed_conformance, encoding, debug,
                                 verbose)

            # store the result
            self.result_queue.put((job, osis))


def main(args=None):
    global BOOK_DICT

    num_processes = max(1, multiprocessing.cpu_count())
    num_jobs = num_processes
    lang_code = 'und'

    encoding = ''
    relaxed_conformance = False
    input_files_index = 2  # This marks the point in the sys.argv array, after which all values represent USFM files to be converted.
    usfm_doc_list = list()

    if '-v' in sys.argv:
        verbose = True
        input_files_index += 1
    else:
        verbose = False

    if '-x' in sys.argv:
        validate_xml = False
        input_files_index += 1
    else:
        validate_xml = True

    if '-d' in sys.argv:
        debug = True
        input_files_index += 1
        num_processes = 1
        num_jobs = 1
        verbose = True
    else:
        debug = False

    if '-t' in sys.argv:
        i = sys.argv.index('-t')+1
        if len(sys.argv) < i+1:
            print_usage()
        try:
            num_processes = max(1, int(sys.argv[i]))
            input_files_index += 2  # increment 2, reflecting 2 args for -t
        except ValueError:
            print_usage()

    if '-l' in sys.argv:
        i = sys.argv.index('-l')+1
        if len(sys.argv) < i+1:
            print_usage()
        try:
            lang_code = sys.argv[i]
            input_files_index += 2  # increment 2, reflecting 2 args for -l
        except ValueError:
            print_usage()

    if '-h' in sys.argv or '--help' in sys.argv or len(sys.argv) < 3:
        print_usage()
    else:
        osisWork = sys.argv[1]

        if '-o' in sys.argv:
            i = sys.argv.index('-o')+1
            if len(sys.argv) < i+1:
                print_usage()
            osis_filename = sys.argv[i]
            input_files_index += 2  # increment 2, reflecting 2 args for -o
        else:
            osis_filename = osisWork + '.osis.xml'

        if '-e' in sys.argv:
            i = sys.argv.index('-e')+1
            if len(sys.argv) < i+1:
                print_usage()
            encoding = sys.argv[i]
            input_files_index += 2  # increment 2, reflecting 2 args for -e

        if '-r' in sys.argv:
            relaxed_conformance = True
            book_dict = dict(list(BOOK_DICT.items()) +
                             list(ADD_BOOK_DICT.items()))
            input_files_index += 1

        if '-s' in sys.argv:
            i = sys.argv.index('-s')+1
            if len(sys.argv) < i+1:
                print_usage()
            if sys.argv[i].startswith('a'):
                sortKey = None
                print('Sorting book files alphanumerically')
            elif sys.argv[i].startswith('na'):
                sortKey = key_natural
                print('Sorting book files naturally')
            elif sys.argv[i].startswith('c'):
                sortKey = key_canon
                print('Sorting book files canonically')
            elif sys.argv[i].startswith('u'):
                sortKey = key_usfm
                print('Sorting book files by USFM book number')
            elif sys.argv[i].startswith('random'):  # for testing only
                sortKey = lambda filename: int(random.random()*256)
                print('Sorting book files randomly')
            else:
                sortKey = key_supplied
                print('Leaving book files unsorted, in the order in which they were supplied')
            input_files_index += 2  # increment 2, reflecting 2 args for -s
        else:
            sortKey = key_natural
            print('Sorting book files naturally')

        usfm_doc_list = sys.argv[input_files_index:]

        for filename in usfm_doc_list:
            read_identifiers_from_osis(filename)
        usfm_doc_list = sorted(usfm_doc_list, key=sortKey)

        # run
        # load up work queue
        work_queue = multiprocessing.Queue()
        for job in usfm_doc_list:
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
        for i in usfm_doc_list:
            k, v = result_queue.get()
            osisSegment[k] = v

        print('Assembling OSIS document')
        osis_doc = '<osis xmlns="http://www.bibletechnologies.net/2003/OSIS/namespace" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.bibletechnologies.net/2003/OSIS/namespace http://www.bibletechnologies.net/osisCore.'+osisVersion+'.xsd">\n<osisText osisRefWork="Bible" xml:lang="' + lang_code + '" osisIDWork="' + osisWork + '">\n<header>\n<work osisWork="' + osisWork + '"/>\n</header>\n'

        unhandled_tags = set()
        for doc in usfm_doc_list:
            unhandled_tags |= set(re.findall(r'(\\[^\s]*)', osisSegment[doc]))
            osis_doc += osisSegment[doc]

        osis_doc += '</osisText>\n</osis>\n'

        if validate_xml:
            try:
                from lxml import etree
                print('Validating XML...')
                osis_schema = pkgutil.get_data('usfm2osis', 'schemas/osisCore.2.1.1.xsd').decode("utf-8")
                replacement = os.path.dirname(usfm2osis.__file__)+'/schemas/xml.xsd'
                osis_schema = bytes(osis_schema.replace('http://www.w3.org/2001/xml.xsd', replacement), 'utf-8')
                osis_parser = etree.XMLParser(schema=etree.XMLSchema(etree.XML(osis_schema)),
                                              no_network=True)
                etree.fromstring(osis_doc, osis_parser)
                print('XML Valid')
            except ImportError:
                print('For schema validation, install lxml')
            except etree.XMLSyntaxError as error_val:
                print('XML Validation error: ' + str(error_val))

        osis_file = codecs.open(osis_filename, 'w', 'utf-8')
        osis_file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        osis_file.write(osis_doc)

        print('Done!')

        if unhandled_tags:
            print('')
            print(('Unhandled USFM tags: ' + ', '.join(sorted(unhandled_tags)) +
                   ' (' + str(len(unhandled_tags)) + ' total)'))
            if not relaxed_conformance:
                print('Consider using the -r option for relaxed markup processing')

if __name__ == "__main__":
    main()
