#!/usr/bin/env python

import c3
import urllib

try:
  data = open("c4.txt").read()
except:
  data = urllib.urlopen("https://gist.github.com/tqbf/3132713/raw/40da378d42026a0731ee1cd0b2bd50f66aabac5b/gistfile1.txt").read()
  open("c4.txt","w").write(data)

for l in data.split("\n"):
  txt = c3.fcxor(l.rstrip().decode('hex'))
  if txt != None:
    print txt
