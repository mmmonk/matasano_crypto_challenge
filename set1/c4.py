#!/usr/bin/env python

import urllib
import c3

for l in urllib.URLopener().open("https://gist.github.com/tqbf/3132713/raw/40da378d42026a0731ee1cd0b2bd50f66aabac5b/gistfile1.txt").readlines():
  txt = c3.fcxor(l.rstrip().decode('hex'))
  if txt != None:
    print txt
