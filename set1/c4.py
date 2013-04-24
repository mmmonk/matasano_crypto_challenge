#!/usr/bin/env python

import c3

for l in open("gistfile1.txt").readlines():
  c3.fcxor(l.rstrip())
