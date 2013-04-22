#!/usr/bin/env python

import string

ct = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736".decode('hex')


for x in range(256):
  mesg = []
  for i in range(len(ct)):
    mesg.append(chr(x^ord(ct[i])))
    if not mesg[-1] in string.printable:
      break
    if i + 1 == len(ct):
      print str(x)+" "+"".join(mesg)
      chars = dict()
      for c in mesg:
        chars[c] = chars.get(c,0) + 1
      print chars

