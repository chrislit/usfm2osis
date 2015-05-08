# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
def readfile(fn):
    """Read fn and return the contents."""
    with open(path.join(here, fn), 'r', encoding='utf-8') as f:
        return f.read()

setup(
    name = 'usfm2osis',
    packages = find_packages(exclude=['tests*']),
    version = '0.6.1',
    description = 'Tools for converting Bibles from USFM to OSIS XML',
    author = 'Christopher C. Little',
    author_email = 'chrisclittle+usfm2osis@gmail.com',
    url = 'https://github.com/chrislit/usfm2osis',
    download_url = 'https://github.com/chrislit/usfm2osis/archive/master.zip',
    keywords = ['OSIS', 'USFM', 'Bible'],
    license='GPLv3+',
    classifiers = [
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Intended Audience :: Religion',
        'Intended Audience :: Developers',
        'Topic :: Religion',
        'Topic :: Text Processing :: Markup :: XML'
    ],
    long_description = '\n\n'.join([readfile(f) for f in ('README.rst',)]),
    scripts=['scripts/usfm2osis.py', 'scripts/usfmtags.py']
)
