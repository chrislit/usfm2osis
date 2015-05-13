#!/bin/sh

sudo rm -rf ./usfm2osis.egg-info
sudo rm -rf ./dist

sudo rm -rf ./build
python setup.py build
sudo python setup.py install

sudo rm -rf ./build
python3 setup.py build
sudo python3 setup.py install

nosetests -v --with-coverage --cover-erase --cover-html --cover-branches --cover-package=usfm2osis .
nosetests3 -v --with-coverage --cover-erase --cover-html --cover-branches --cover-package=usfm2osis .

pylint --rcfile=pylint.rc usfm2osis > pylint.log
pep8 -v --statistics --exclude=.git,__pycache__,build . > pep8.log

sudo python3 setup.py sdist
sudo python3 setup.py bdist_wheel
