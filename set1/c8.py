#!/usr/bin/env python

import urllib
from Crypto.Cipher import AES

def findecb(cte,blksize=16):
  ct = cte.decode('hex')
  a = dict()
  for i in range(0,len(ct),blksize):
    c = ct[i:i+blksize]
    a[c] = a.get(c,0) + 1
    if a[c] > 1:
      return cte

for l in urllib.URLopener().open("https://gist.github.com/tqbf/3132928/raw/6f74d4131d02dee3dd0766bd99a6b46c965491cc/gistfile1.txt").readlines():
  ct = findecb(l.rstrip())
  if ct != None:
    print ct

