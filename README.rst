usfm2osis
=========

.. image:: https://travis-ci.org/chrislit/usfm2osis.svg
    :target: https://travis-ci.org/chrislit/usfm2osis
    :alt: Build Status

.. image:: https://coveralls.io/repos/chrislit/usfm2osis/badge.svg
    :target: https://coveralls.io/r/chrislit/usfm2osis
    :alt: Coverage Status

.. image:: https://img.shields.io/pypi/v/usfm2osis.svg
    :target: https://pypi.python.org/pypi/usfm2osis
    :alt: PyPI

.. image:: https://readthedocs.org/projects/usfm2osis/badge/?version=latest
    :target: https://usfm2osis.readthedocs.org/en/latest/
    :alt: Documentation Status

Tools for converting Bibles from USFM to OSIS XML

::

    Usage: usfm2osis <osisWork> [OPTION] ...  <USFM filename|wildcard> ...
      -h, --help       print this usage information
      -d               debug mode (single-threaded, verbose output)
      -e ENCODING      input encoding override (default is to read the USFM file's
                         \ide value or assume UTF-8 encoding in its absence)
      -o FILENAME      output filename (default is: <osisWork>.osis.xml)
      -r               enable relaxed markup processing (for non-standard USFM)
      -s MODE          set book sorting mode: natural (default), alpha, canonical,
                         usfm, random, none
      -t NUM           set the number of separate processes to use (your maximum
                          thread count by default)
      -l LANG          set the language value to a BCP 47 code (\'und\' by default)
      -v               verbose feedback
      -x               disable XML validation

    As an example, if you want to generate the osisWork <Bible.KJV> and your USFM
      are located in the ./KJV folder, enter:
        python usfm2osis Bible.KJV ./KJV/*.usfm
