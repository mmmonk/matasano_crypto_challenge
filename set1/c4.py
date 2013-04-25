#!/usr/bin/env python

import c3

for l in open("c4.txt").readlines():
  txt = c3.fcxor(l.rstrip().decode('hex'))
  if txt != None:
    print txt
