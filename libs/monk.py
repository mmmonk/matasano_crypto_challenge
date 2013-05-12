#!/usr/bin/env python

def bindiff(a,b,bl=32):
  a = bin(a).replace("0b","").zfill(bl)
  b = bin(b).replace("0b","").zfill(bl)
  out = ""
  for i in range(bl):
    if a[i] == b[i]:
      out += "."
    else:
      out += "x"
  return out
