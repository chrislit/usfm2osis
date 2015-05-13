#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import codecs

loremText = open('lorem.txt').read().strip()

# lorem = list(set(re.sub(r'[^a-zA-Z ]', r' ', loremText).lower().split()))
# utext = u'\\v adhkljfsaa Мыа но льабятюр дэлььикат 1234άτεψε τις λέξεις 5473'
lorem = loremText.split()


def loremize(w):
    global i
    if i >= len(lorem):
        i = 0
    if re.search(r'[\d\\_]', w, flags=re.U):
        return w
    elif not re.match(r'\w+$', w, flags=re.U):
        return w
    else:
        i += 1
        return lorem[i-1]

for filename in sorted(os.listdir('usfmSamples_orig')):
    infile = codecs.open('usfmSamples_orig/'+filename, 'r', 'utf-8')
    outfile = codecs.open('usfmSamples/'+filename, 'w', 'utf-8')
    i = 0

    print filename
    for l in infile:
        if re.search(r'(\ide?|\periph)\b', l):
            outfile.write(l)
        else:
            outfile.write(' '.join(map(loremize, l.split()))+'\n')
