#!/usr/bin/env python

def findecb(cte,blksize=16):
  ct = cte.decode('hex')
  a = dict()
  for i in range(0,len(ct),blksize):
    c = ct[i:i+blksize]
    a[c] = a.get(c,0) + 1
    if a[c] > 1:
      return cte

for l in open("c8.txt").readlines():
  ct = findecb(l.rstrip())
  if ct != None:
    print ct

