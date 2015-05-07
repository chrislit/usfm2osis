usfm2osis
=========

[![Build Status](https://travis-ci.org/chrislit/usfm2osis.svg)](https://travis-ci.org/chrislit/usfm2osis)
[![Coverage Status](https://coveralls.io/repos/chrislit/usfm2osis/badge.svg)](https://coveralls.io/r/chrislit/usfm2osis)
[![Documentation Status](https://readthedocs.org/projects/usfm2osis/badge/?version=latest)](https://usfm2osis.readthedocs.org/en/latest/)

Python scripts for converting USFM to OSIS XML

    Usage: usfm2osis.py <osisWork> [OPTION] ...  <USFM filename|wildcard> ...')
      -d               debug mode (single-threaded, verbose output)
      -e ENCODING      input encoding override (default is to read the USFM file's
                         \ide value or assume UTF-8 encoding in its absence)
      -h, --help       print this usage information
      -o FILENAME      output filename (default is: <osisWork>.osis.xml)
      -r               enable relaxed markup processing (for non-standard USFM)
      -s mode          set book sorting mode: natural (default), alpha, canonical,
                         usfm, random, none
      -v               verbose feedback
      -x               disable XML validation

    As an example, if you want to generate the osisWork <Bible.KJV> and your USFM
      are located in the ./KJV folder, enter:
        python usfm2osis.py Bible.KJV ./KJV/*.usfm
